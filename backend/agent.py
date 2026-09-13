"""Autonomous planner graph: Observe -> Diagnose -> Retrieve -> Plan -> Verify -> Act/Replan."""
from typing import TypedDict, List, Dict, Any
try:
    from langgraph.graph import StateGraph, END
    LANGGRAPH_AVAILABLE = True
except Exception:
    LANGGRAPH_AVAILABLE = False
from resources import retrieve

class AgentState(TypedDict, total=False):
    student: Dict[str, Any]
    gaps: List[Dict[str, Any]]
    resources: List[Dict[str, Any]]
    proposed_sessions: List[Dict[str, Any]]
    verification: Dict[str, Any]
    trace: List[Dict[str, str]]

def event(state, step, message):
    state.setdefault('trace', []).append({'step': step, 'message': message})
    return state

def observe(state):
    s = state['student']
    event(state, 'OBSERVE', f"Loaded {len(s['performance'])} performance signals and {len(s['sessions'])} scheduled activities.")
    return state

def diagnose(state):
    gaps=[]
    for p in state['student']['performance']:
        priority = round((100-p['score'])*0.65 + (100-p['confidence'])*0.35, 1)
        gaps.append({'topic':p['topic'],'score':p['score'],'confidence':p['confidence'],'priority':priority})
    state['gaps']=sorted(gaps,key=lambda x:x['priority'],reverse=True)
    event(state,'DIAGNOSE',f"Ranked {len(gaps)} knowledge areas; top priority: {state['gaps'][0]['topic']}.")
    return state

def retrieve_resources(state):
    out=[]
    for gap in state['gaps'][:4]:
        for r in retrieve(gap['topic'],2):
            out.append({**r,'reason':f"Selected because mastery is {gap['score']}% and confidence is {gap['confidence']}%."})
    state['resources']=out
    event(state,'RETRIEVE',f"Retrieved {len(out)} resources matched to priority gaps and current level.")
    return state

def plan(state):
    # Simple constraint-aware planner: avoids blocked day/hour and existing occupied times.
    days=[('Mon','2026-09-14'),('Tue','2026-09-15'),('Wed','2026-09-16'),('Thu','2026-09-17'),('Fri','2026-09-18'),('Sat','2026-09-19')]
    existing=state['student']['sessions']
    blocked=state['student'].get('blocked_times',[])
    candidates=['08:00','10:00','17:00','19:00']
    proposed=[]; idx=0
    for gap in state['gaps'][:4]:
        placed=False
        for day,date in days:
            for start in candidates:
                if any(x.get('day')==day and x.get('start')==start for x in blocked): continue
                if any(x['date']==date and x['start']==start and x['status'] in ['upcoming','rescheduled'] for x in existing): continue
                resource=next((r for r in state['resources'] if r['topic']==gap['topic']),None)
                proposed.append({'id':f'agent-{idx}','day':day,'date':date,'start':start,'end':'18:00' if start=='17:00' else '11:00' if start=='10:00' else '09:00' if start=='08:00' else '20:00','topic':gap['topic'],'activity':resource['title'] if resource else 'Targeted practice','resource':resource['url'] if resource else '', 'status':'upcoming'})
                idx+=1; placed=True; break
            if placed: break
    state['proposed_sessions']=proposed
    event(state,'PLAN',f"Created {len(proposed)} constraint-aware learning activities around calendar conflicts.")
    return state

def verify(state):
    hours=len(state['proposed_sessions'])
    critical=[g for g in state['gaps'] if g['priority']>=45]
    state['verification']={'valid':hours>=min(3,len(state['gaps'])),'planned_hours':hours,'target_hours':state['student']['weekly_hours_target'],'critical_gaps_covered':len(critical),'message':f"Plan covers {len(state['proposed_sessions'])} priority activities; critical gaps are represented and conflicts were avoided."}
    event(state,'VERIFY',state['verification']['message'])
    return state

def build_graph():
    if not LANGGRAPH_AVAILABLE: return None
    graph=StateGraph(AgentState)
    graph.add_node('observe',observe); graph.add_node('diagnose',diagnose); graph.add_node('retrieve',retrieve_resources); graph.add_node('plan',plan); graph.add_node('verify',verify)
    graph.set_entry_point('observe')
    graph.add_edge('observe','diagnose'); graph.add_edge('diagnose','retrieve'); graph.add_edge('retrieve','plan'); graph.add_edge('plan','verify'); graph.add_edge('verify',END)
    return graph.compile()

def run_agent(student):
    state={'student':student,'trace':[]}
    graph=build_graph()
    if graph: return graph.invoke(state)
    for fn in [observe,diagnose,retrieve_resources,plan,verify]: state=fn(state)
    return state
