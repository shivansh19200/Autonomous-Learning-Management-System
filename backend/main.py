from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from models import StudentState, Performance, Session
from agent import run_agent

ROOT=Path(__file__).resolve().parent.parent
app=FastAPI(title='StudyPlanner.agent')
app.mount('/static', StaticFiles(directory=ROOT/'frontend'), name='static')

state=StudentState(
 performance=[
  Performance(topic='Dynamic Programming',score=42,confidence=35,attempts=3),
  Performance(topic='Advanced Graph Algorithms',score=48,confidence=45,attempts=2),
  Performance(topic='Segment Trees / Fenwick Trees',score=58,confidence=55,attempts=2),
  Performance(topic='String Algorithms',score=72,confidence=68,attempts=1)],
 sessions=[
  Session(id='s1',day='Mon',date='2026-09-14',start='17:00',end='18:00',topic='Dynamic Programming',activity='DP Foundations — Memoization patterns',status='completed',score=78),
  Session(id='s2',day='Wed',date='2026-09-16',start='19:00',end='20:00',topic='Dynamic Programming',activity='0/1 Knapsack & variants',status='completed',score=82),
  Session(id='s3',day='Thu',date='2026-09-17',start='18:00',end='19:00',topic='Advanced Graph Algorithms',activity='Graph traversal — DFS/BFS review',status='missed'),
  Session(id='s4',day='Fri',date='2026-09-18',start='17:00',end='18:00',topic='Advanced Graph Algorithms',activity='Dijkstra & Bellman-Ford',status='rescheduled'),
  Session(id='s5',day='Sat',date='2026-09-19',start='10:00',end='11:00',topic='Advanced Graph Algorithms',activity='Dijkstra & Bellman-Ford',status='upcoming')]
)

def payload():
    d=state.model_dump(); d['agent_active']=True
    return d

@app.get('/')
def home(): return FileResponse(ROOT/'frontend'/'index.html')
@app.get('/api/state')
def get_state(): return payload()

@app.post('/api/run-agent')
def run():
    global state
    result=run_agent(state.model_dump())
    state.agent_events=[{'time':datetime.now().strftime('%H:%M:%S'),**x} for x in result['trace']]
    existing_ids={x.id for x in state.sessions}
    for s in result['proposed_sessions']:
        if s['id'] not in existing_ids and not any(x.activity==s['activity'] and x.date==s['date'] for x in state.sessions): state.sessions.append(Session(**s))
    return {'result':result,'state':payload()}

class StatusUpdate(BaseModel): status:str; score:float|None=None
@app.post('/api/session/{session_id}')
def update_session(session_id:str, body:StatusUpdate):
    for s in state.sessions:
        if s.id==session_id:
            s.status=body.status
            if body.score is not None: s.score=body.score
            state.agent_events.insert(0,{'time':datetime.now().strftime('%H:%M:%S'),'step':'TRACK','message':f"Observed {s.activity}: {body.status}. Triggering reassessment."})
            return {'ok':True,'state':payload()}
    raise HTTPException(404,'Session not found')

class Block(BaseModel): day:str; start:str
@app.post('/api/block-time')
def block_time(body:Block):
    state.blocked_times.append(body.model_dump())
    state.agent_events.insert(0,{'time':datetime.now().strftime('%H:%M:%S'),'step':'CONSTRAINT','message':f"New unavailable time: {body.day} {body.start}. Future plan requires replanning."})
    return payload()

class Goal(BaseModel): goal:str; deadline:str; weekly_hours_target:float=10
@app.post('/api/goal')
def set_goal(body:Goal):
    state.goal=body.goal; state.deadline=body.deadline; state.weekly_hours_target=body.weekly_hours_target
    return payload()
