"""Generate an interactive HTML visualization of the TripPlanningFlow.

Run: python -m scripts.visualize_flow
Output: agents/flow_visualization.html
"""

FLOW_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Trip Planning Agent Flow</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: system-ui, -apple-system, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 2rem; }
  h1 { text-align: center; font-size: 1.5rem; margin-bottom: 0.5rem; color: #f1f5f9; }
  .subtitle { text-align: center; font-size: 0.85rem; color: #94a3b8; margin-bottom: 2rem; }
  .flow-container { max-width: 1000px; margin: 0 auto; position: relative; }
  .step { display: flex; align-items: flex-start; margin-bottom: 1.5rem; position: relative; }
  .step-num { flex-shrink: 0; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.85rem; margin-right: 1rem; margin-top: 0.5rem; }
  .step-content { flex: 1; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; transition: all 0.2s; }
  .step-content:hover { border-color: #60a5fa; box-shadow: 0 0 20px rgba(96,165,250,0.1); }
  .step-label { font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem; }
  .step-desc { font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.75rem; }
  .decorator { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-family: monospace; font-weight: 600; margin-bottom: 0.5rem; }
  .dec-start { background: #065f46; color: #6ee7b7; }
  .dec-router { background: #7c2d12; color: #fdba74; }
  .dec-listen { background: #1e3a5f; color: #93c5fd; }
  .agents-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
  .agent-chip { background: #0f172a; border: 1px solid #475569; border-radius: 6px; padding: 4px 10px; font-size: 0.75rem; color: #cbd5e1; display: flex; align-items: center; gap: 4px; }
  .agent-chip .icon { font-size: 0.85rem; }
  .crew-name { font-size: 0.75rem; color: #60a5fa; font-weight: 600; margin-top: 0.5rem; }
  .branch { display: flex; gap: 1rem; margin-top: 0.5rem; }
  .branch-item { flex: 1; background: #0f172a; border: 1px solid #475569; border-radius: 8px; padding: 0.75rem; }
  .branch-label { font-size: 0.75rem; font-weight: 600; color: #fbbf24; margin-bottom: 0.5rem; }
  .arrow { text-align: center; color: #475569; font-size: 1.5rem; margin: 0.5rem 0; }
  .legend { max-width: 1000px; margin: 2rem auto 0; display: flex; gap: 1.5rem; justify-content: center; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; color: #94a3b8; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; }
  .conditional { border-left: 3px solid #f59e0b; }
  .step-num.s1 { background: #065f46; color: #6ee7b7; }
  .step-num.s2 { background: #7c2d12; color: #fdba74; }
  .step-num.s3 { background: #1e3a5f; color: #93c5fd; }
  .step-num.s4 { background: #4c1d95; color: #c4b5fd; }
  .step-num.s5 { background: #831843; color: #f9a8d4; }
  .step-num.s6 { background: #164e63; color: #67e8f9; }
  .state-panel { max-width: 1000px; margin: 2rem auto 0; background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; }
  .state-panel h3 { font-size: 0.9rem; color: #f1f5f9; margin-bottom: 0.75rem; }
  .state-fields { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.5rem; }
  .state-field { font-size: 0.75rem; color: #94a3b8; background: #0f172a; padding: 4px 8px; border-radius: 4px; font-family: monospace; }
  .state-field .type { color: #60a5fa; }
</style>
</head>
<body>
<h1>TripPlanningFlow — Agent Orchestration</h1>
<p class="subtitle">CrewAI Flow with 6 crews, 14 agents | @start → @router → @listen chain</p>

<div class="flow-container">

  <!-- Step 1: Parse Intent -->
  <div class="step">
    <div class="step-num s1">1</div>
    <div class="step-content">
      <span class="decorator dec-start">@start()</span>
      <div class="step-label">parse_intent()</div>
      <div class="step-desc">Extract travel intent slots from user message. Parses JSON for destination, dates, travelers, budget, preferences.</div>
      <div class="crew-name">IntentCrew</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">🧠</span> Intent Parser</div>
      </div>
    </div>
  </div>

  <div class="arrow">↓</div>

  <!-- Step 2: Router -->
  <div class="step">
    <div class="step-num s2">2</div>
    <div class="step-content">
      <span class="decorator dec-router">@router(parse_intent)</span>
      <div class="step-label">route_after_intent()</div>
      <div class="step-desc">Decision node: checks if intent slots are complete, then routes by destination.</div>
      <div class="branch">
        <div class="branch-item conditional">
          <div class="branch-label">→ "ask_user" (incomplete)</div>
          <div style="font-size:0.75rem;color:#94a3b8">Missing: destination, dates, or travelers</div>
        </div>
        <div class="branch-item">
          <div class="branch-label">→ "plan_japan"</div>
          <div style="font-size:0.75rem;color:#94a3b8">destination contains "japan"</div>
        </div>
        <div class="branch-item">
          <div class="branch-label">→ "plan_taiwan"</div>
          <div style="font-size:0.75rem;color:#94a3b8">destination contains "taiwan"</div>
        </div>
      </div>
    </div>
  </div>

  <div class="arrow">↓ ↓ ↓</div>

  <!-- Step 3a: Clarifying -->
  <div class="step">
    <div class="step-num s3">⬅</div>
    <div class="step-content conditional">
      <span class="decorator dec-listen">@listen("ask_user")</span>
      <div class="step-label">ask_clarifying_questions()</div>
      <div class="step-desc">Generates questions for missing required fields. Sets final_itinerary to the question text and returns early (no downstream crews run).</div>
    </div>
  </div>

  <!-- Step 3b: Japan -->
  <div class="step">
    <div class="step-num s3">3a</div>
    <div class="step-content">
      <span class="decorator dec-listen">@listen("plan_japan")</span>
      <div class="step-label">plan_japan_trip()</div>
      <div class="step-desc">Day-by-day Japan itinerary with hotels, trains, festivals, and optional skiing.</div>
      <div class="crew-name">JapanCrew (4-5 agents)</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">📋</span> Itinerary Specialist</div>
        <div class="agent-chip"><span class="icon">🏨</span> Hotel Expert</div>
        <div class="agent-chip"><span class="icon">🚄</span> Train Specialist</div>
        <div class="agent-chip"><span class="icon">🎎</span> Festival Researcher</div>
        <div class="agent-chip"><span class="icon">⛷️</span> Skiing Coach <small>(conditional)</small></div>
      </div>
    </div>
  </div>

  <!-- Step 3c: Taiwan -->
  <div class="step">
    <div class="step-num s3">3b</div>
    <div class="step-content">
      <span class="decorator dec-listen">@listen("plan_taiwan")</span>
      <div class="step-label">plan_taiwan_trip()</div>
      <div class="step-desc">Day-by-day Taiwan itinerary with hotels, trains, and festivals.</div>
      <div class="crew-name">TaiwanCrew (4 agents)</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">📋</span> Itinerary Specialist</div>
        <div class="agent-chip"><span class="icon">🏨</span> Hotel Expert</div>
        <div class="agent-chip"><span class="icon">🚅</span> Train Specialist</div>
        <div class="agent-chip"><span class="icon">🏮</span> Festival Researcher</div>
      </div>
    </div>
  </div>

  <div class="arrow">↓</div>

  <!-- Step 4: Booking -->
  <div class="step">
    <div class="step-num s4">4</div>
    <div class="step-content">
      <span class="decorator dec-listen">@listen(plan_japan_trip, plan_taiwan_trip)</span>
      <div class="step-label">book_flights_and_esim()</div>
      <div class="step-desc">Search flights and recommend eSIM data plans. Runs after either destination crew finishes.</div>
      <div class="crew-name">BookingCrew (2 agents)</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">✈️</span> Flight Search Specialist</div>
        <div class="agent-chip"><span class="icon">📱</span> eSIM Card Specialist</div>
      </div>
    </div>
  </div>

  <div class="arrow">↓</div>

  <!-- Step 5: Advisory -->
  <div class="step">
    <div class="step-num s5">5</div>
    <div class="step-content">
      <span class="decorator dec-listen">@listen(book_flights_and_esim)</span>
      <div class="step-label">get_advisory_info()</div>
      <div class="step-desc">Currency exchange tips and family travel advice (conditional on children_ages).</div>
      <div class="crew-name">AdvisoryCrew (1-2 agents)</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">💱</span> Currency Exchange Specialist</div>
        <div class="agent-chip"><span class="icon">👨‍👩‍👧</span> Family Travel Advisor <small>(conditional)</small></div>
      </div>
    </div>
  </div>

  <div class="arrow">↓</div>

  <!-- Step 6: Synthesis -->
  <div class="step">
    <div class="step-num s6">6</div>
    <div class="step-content">
      <span class="decorator dec-listen">@listen(get_advisory_info)</span>
      <div class="step-label">synthesize_final_itinerary()</div>
      <div class="step-desc">Combines all data (itinerary, hotels, flights, currency, family advice) into a polished markdown response.</div>
      <div class="crew-name">SynthesisCrew (1 agent)</div>
      <div class="agents-grid">
        <div class="agent-chip"><span class="icon">✍️</span> Travel Itinerary Writer</div>
      </div>
    </div>
  </div>
</div>

<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#6ee7b7"></div> @start — entry point</div>
  <div class="legend-item"><div class="legend-dot" style="background:#fdba74"></div> @router — conditional branching</div>
  <div class="legend-item"><div class="legend-dot" style="background:#93c5fd"></div> @listen — event-driven step</div>
  <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;width:3px;height:16px;border-radius:2px"></div> conditional path</div>
</div>

<div class="state-panel">
  <h3>TripPlanningState (carried through all steps)</h3>
  <div class="state-fields">
    <div class="state-field">user_message <span class="type">str</span></div>
    <div class="state-field">intent <span class="type">IntentSlots</span></div>
    <div class="state-field">slots_complete <span class="type">bool</span></div>
    <div class="state-field">itinerary_data <span class="type">dict?</span></div>
    <div class="state-field">hotel_data <span class="type">dict?</span></div>
    <div class="state-field">flight_data <span class="type">dict?</span></div>
    <div class="state-field">currency_data <span class="type">dict?</span></div>
    <div class="state-field">family_advice <span class="type">dict?</span></div>
    <div class="state-field">final_itinerary <span class="type">str?</span></div>
    <div class="state-field">clarifying_questions <span class="type">list?</span></div>
  </div>
</div>

<div class="state-panel" style="margin-top:1rem">
  <h3>IntentSlots (extracted from user messages)</h3>
  <div class="state-fields">
    <div class="state-field">destination <span class="type">str?</span></div>
    <div class="state-field">start_date <span class="type">str?</span></div>
    <div class="state-field">end_date <span class="type">str?</span></div>
    <div class="state-field">duration_days <span class="type">int?</span></div>
    <div class="state-field">num_travelers <span class="type">int?</span></div>
    <div class="state-field">children_ages <span class="type">list[int]?</span></div>
    <div class="state-field">budget_usd <span class="type">float?</span></div>
    <div class="state-field">preferences <span class="type">list[str]?</span></div>
    <div class="state-field">trip_style <span class="type">str?</span></div>
    <div class="state-field">origin_city <span class="type">str?</span></div>
    <div class="state-field">has_skiing <span class="type">bool</span></div>
    <div class="state-field">needs_family_advice <span class="type">bool</span></div>
  </div>
  <div style="margin-top:0.75rem;font-size:0.75rem;color:#94a3b8">
    <strong>is_complete</strong> requires: destination + (duration_days OR start_date+end_date) + num_travelers
  </div>
</div>

</body>
</html>
"""

if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "flow_visualization.html"
    out.write_text(FLOW_HTML)
    print(f"Generated: {out}")
