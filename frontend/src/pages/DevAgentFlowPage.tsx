import { useEffect, useRef, useState } from "react";
import { chatApi } from "../lib/api";
import type { ChatSession } from "../lib/types";
import { useFlowEvents, type TimelineEvent } from "../hooks/useFlowEvents";

/* ─── Agent/crew definitions derived from agents/orchestrator/ ───────────── */
const CREWS = [
  {
    id: "intent",
    name: "IntentCrew",
    step: 1,
    decorator: "@start()",
    method: "parse_intent()",
    desc: "Extract travel intent from user message — destination, dates, travelers, budget, preferences.",
    agents: [{ icon: "🧠", name: "Intent Parser" }],
    color: "emerald",
  },
  {
    id: "router",
    name: "Router",
    step: 2,
    decorator: "@router(parse_intent)",
    method: "route_after_intent()",
    desc: 'Routes by slots completeness and destination → "ask_user" | "plan_japan" | "plan_taiwan".',
    agents: [],
    color: "amber",
  },
  {
    id: "japan",
    name: "JapanCrew",
    step: 3,
    decorator: '@listen("plan_japan")',
    method: "plan_japan_trip()",
    desc: "Day-by-day Japan itinerary with hotels, trains, festivals, and optional skiing.",
    agents: [
      { icon: "📋", name: "Itinerary Specialist" },
      { icon: "🏨", name: "Hotel Expert" },
      { icon: "🚄", name: "Train Specialist" },
      { icon: "🎎", name: "Festival Researcher" },
      { icon: "⛷️", name: "Skiing Coach", conditional: true },
    ],
    color: "blue",
  },
  {
    id: "taiwan",
    name: "TaiwanCrew",
    step: 3,
    decorator: '@listen("plan_taiwan")',
    method: "plan_taiwan_trip()",
    desc: "Day-by-day Taiwan itinerary with hotels, HSR trains, and festivals.",
    agents: [
      { icon: "📋", name: "Itinerary Specialist" },
      { icon: "🏨", name: "Hotel Expert" },
      { icon: "🚅", name: "Train Specialist" },
      { icon: "🏮", name: "Festival Researcher" },
    ],
    color: "blue",
  },
  {
    id: "booking",
    name: "BookingCrew",
    step: 4,
    decorator: "@listen(plan_japan_trip, plan_taiwan_trip)",
    method: "book_flights_and_esim()",
    desc: "Search flights and recommend eSIM data plans.",
    agents: [
      { icon: "✈️", name: "Flight Search Specialist" },
      { icon: "📱", name: "eSIM Card Specialist" },
    ],
    color: "violet",
  },
  {
    id: "advisory",
    name: "AdvisoryCrew",
    step: 5,
    decorator: "@listen(book_flights_and_esim)",
    method: "get_advisory_info()",
    desc: "Currency exchange tips and family travel advice.",
    agents: [
      { icon: "💱", name: "Currency Exchange Specialist" },
      { icon: "👨‍👩‍👧", name: "Family Travel Advisor", conditional: true },
    ],
    color: "pink",
  },
  {
    id: "synthesis",
    name: "SynthesisCrew",
    step: 6,
    decorator: "@listen(get_advisory_info)",
    method: "synthesize_final_itinerary()",
    desc: "Combines all data into a polished markdown travel plan.",
    agents: [{ icon: "✍️", name: "Travel Itinerary Writer" }],
    color: "cyan",
  },
] as const;

type Crew = (typeof CREWS)[number];

const INTENT_FIELDS = [
  "destination",
  "start_date",
  "end_date",
  "duration_days",
  "num_travelers",
  "children_ages",
  "budget_usd",
  "preferences",
  "trip_style",
  "origin_city",
];

const colorMap: Record<string, { bg: string; border: string; text: string; badge: string; ring: string }> = {
  emerald: { bg: "bg-emerald-900/30", border: "border-emerald-700/50", text: "text-emerald-400", badge: "bg-emerald-800 text-emerald-300", ring: "ring-emerald-500/40" },
  amber:   { bg: "bg-amber-900/30",   border: "border-amber-700/50",   text: "text-amber-400",   badge: "bg-amber-800 text-amber-300",   ring: "ring-amber-500/40" },
  blue:    { bg: "bg-blue-900/30",     border: "border-blue-700/50",    text: "text-blue-400",     badge: "bg-blue-800 text-blue-300",     ring: "ring-blue-500/40" },
  violet:  { bg: "bg-violet-900/30",   border: "border-violet-700/50",  text: "text-violet-400",   badge: "bg-violet-800 text-violet-300", ring: "ring-violet-500/40" },
  pink:    { bg: "bg-pink-900/30",     border: "border-pink-700/50",    text: "text-pink-400",     badge: "bg-pink-800 text-pink-300",     ring: "ring-pink-500/40" },
  cyan:    { bg: "bg-cyan-900/30",     border: "border-cyan-700/50",    text: "text-cyan-400",     badge: "bg-cyan-800 text-cyan-300",     ring: "ring-cyan-500/40" },
};

/* ─── Visual state ───────────────────────────────────────────────────────── */
type CrewVisualState = "idle" | "active" | "done" | "error";

function getCrewState(
  crewId: string,
  activeCrews: Set<string>,
  doneCrews: Set<string>,
  errorCrews: Set<string>,
): CrewVisualState {
  if (errorCrews.has(crewId)) return "error";
  if (activeCrews.has(crewId)) return "active";
  if (doneCrews.has(crewId)) return "done";
  return "idle";
}

/* ─── CrewCard ───────────────────────────────────────────────────────────── */
function CrewCard({ crew, visualState }: { crew: Crew; visualState: CrewVisualState }) {
  const c = colorMap[crew.color];

  const borderClass =
    visualState === "active"  ? `${c.border} ring-2 ${c.ring} animate-pulse` :
    visualState === "done"    ? "border-green-500/60 ring-2 ring-green-500/30" :
    visualState === "error"   ? "border-red-500/60 ring-2 ring-red-500/30" :
    "border-gray-700/50";

  const statusIcon =
    visualState === "active" ? "⏳" :
    visualState === "done"   ? "✅" :
    visualState === "error"  ? "❌" :
    null;

  return (
    <div className={`rounded-xl border p-4 transition-all duration-300 ${c.bg} ${borderClass}`}>
      <div className="flex items-start justify-between">
        <div>
          <span className={`inline-block rounded px-2 py-0.5 text-xs font-mono font-semibold ${c.badge}`}>
            {crew.decorator}
          </span>
          <h3 className={`mt-1 font-semibold ${c.text}`}>{crew.method}</h3>
          <p className="mt-0.5 text-xs text-gray-400">{crew.desc}</p>
        </div>
        <div className="flex items-center gap-2">
          {statusIcon && <span className="text-lg">{statusIcon}</span>}
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gray-800 text-sm font-bold text-gray-300">
            {crew.step}
          </div>
        </div>
      </div>
      {crew.agents.length > 0 && (
        <div className="mt-3">
          <div className="mb-1 text-xs font-semibold text-gray-500">{crew.name}</div>
          <div className="flex flex-wrap gap-1.5">
            {crew.agents.map((a) => (
              <span
                key={a.name}
                className={`inline-flex items-center gap-1 rounded-md border border-gray-700 bg-gray-800/60 px-2 py-0.5 text-xs text-gray-300 ${
                  "conditional" in a && a.conditional ? "opacity-60" : ""
                }`}
              >
                {a.icon} {a.name}
                {"conditional" in a && a.conditional && (
                  <span className="text-[10px] text-amber-500">(if)</span>
                )}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ─── Timeline entry ─────────────────────────────────────────────────────── */
function TimelineEntry({ event }: { event: TimelineEvent }) {
  const statusColor =
    event.status === "active" ? "bg-blue-500" :
    event.status === "done"   ? "bg-green-500" :
    "bg-red-500";

  const time = new Date(event.ts * 1000).toLocaleTimeString();
  const crews = event.crew
    ? Array.isArray(event.crew) ? event.crew.join(", ") : event.crew
    : "—";

  return (
    <div className="flex items-start gap-3 py-1.5 text-xs">
      <span className="w-16 shrink-0 text-gray-500">{time}</span>
      <span className={`mt-0.5 h-2 w-2 shrink-0 rounded-full ${statusColor}`} />
      <span className="w-28 shrink-0 font-mono text-gray-400">{event.step}</span>
      <span className="w-24 shrink-0 text-gray-500">{crews}</span>
      <span className="text-gray-300">{event.message}</span>
    </div>
  );
}

/* ─── Main page ──────────────────────────────────────────────────────────── */
export function DevAgentFlowPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const timelineEndRef = useRef<HTMLDivElement>(null);

  const flow = useFlowEvents(selectedSessionId);

  // Fetch available sessions on mount
  useEffect(() => {
    chatApi.listSessions().then(({ data }) => setSessions(data)).catch(() => {});
  }, []);

  // Auto-scroll timeline
  useEffect(() => {
    timelineEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [flow.events.length]);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200">
      <div className="mx-auto max-w-5xl px-4 py-8">
        {/* Header + Session selector */}
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-white">Agent Orchestrator Flow</h1>
          <p className="mt-1 text-sm text-gray-500">
            CrewAI Flow: 6 crews, 14 agents | Real-time monitoring
          </p>
        </div>

        <div className="mb-6 flex flex-wrap items-center justify-center gap-3">
          <select
            className="rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-gray-200 focus:border-blue-500 focus:outline-none"
            value={selectedSessionId ?? ""}
            onChange={(e) => setSelectedSessionId(e.target.value || null)}
          >
            <option value="">Select a session to monitor...</option>
            {sessions.map((s) => (
              <option key={s.id} value={s.id}>
                {s.title} ({s.id.slice(0, 8)}...)
              </option>
            ))}
          </select>

          {/* Connection status indicator */}
          <div className="flex items-center gap-2 text-xs text-gray-400">
            <span
              className={`h-2.5 w-2.5 rounded-full ${
                flow.connected ? "bg-green-500 animate-pulse" : "bg-gray-600"
              }`}
            />
            {flow.connected ? "Connected" : selectedSessionId ? "Waiting..." : "No session"}
          </div>
        </div>

        {/* Flow diagram */}
        <div className="space-y-3">
          {/* Step 1 */}
          <CrewCard
            crew={CREWS[0]}
            visualState={getCrewState("intent", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
          />
          <div className="text-center text-gray-600">↓</div>

          {/* Step 2 - Router */}
          <CrewCard
            crew={CREWS[1]}
            visualState={getCrewState("router", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
          />
          <div className="flex items-center justify-center gap-4 text-xs text-gray-500">
            <span className="rounded border border-amber-800/50 bg-amber-900/20 px-2 py-1">
              ← ask_user (incomplete)
            </span>
            <span className="rounded border border-blue-800/50 bg-blue-900/20 px-2 py-1">
              → plan_japan
            </span>
            <span className="rounded border border-blue-800/50 bg-blue-900/20 px-2 py-1">
              → plan_taiwan
            </span>
          </div>

          {/* Step 3 - Destination crews (side by side) */}
          <div className="grid gap-3 md:grid-cols-2">
            <CrewCard
              crew={CREWS[2]}
              visualState={getCrewState("japan", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
            />
            <CrewCard
              crew={CREWS[3]}
              visualState={getCrewState("taiwan", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
            />
          </div>
          <div className="text-center text-gray-600">↓</div>

          {/* Steps 4-6 */}
          <CrewCard
            crew={CREWS[4]}
            visualState={getCrewState("booking", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
          />
          <div className="text-center text-gray-600">↓</div>
          <CrewCard
            crew={CREWS[5]}
            visualState={getCrewState("advisory", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
          />
          <div className="text-center text-gray-600">↓</div>
          <CrewCard
            crew={CREWS[6]}
            visualState={getCrewState("synthesis", flow.activeCrews, flow.doneCrews, flow.errorCrews)}
          />
        </div>

        {/* Live Slots Panel */}
        <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900 p-5">
          <h3 className="mb-3 text-sm font-semibold text-gray-300">
            IntentSlots
            <span className="ml-2 text-xs font-normal text-gray-500">
              is_complete = destination + (duration OR dates) + num_travelers
            </span>
          </h3>
          <div className="flex flex-wrap gap-2">
            {INTENT_FIELDS.map((f) => {
              const value = flow.slots[f];
              const filled = value !== undefined && value !== null;
              return (
                <span
                  key={f}
                  className={`rounded-md px-2.5 py-1 font-mono text-xs transition-colors duration-300 ${
                    filled
                      ? "border border-green-700/50 bg-green-900/30 text-green-300"
                      : "bg-gray-800 text-gray-400"
                  }`}
                >
                  {f}
                  {filled && (
                    <span className="ml-1.5 text-green-400">
                      = {typeof value === "object" ? JSON.stringify(value) : String(value)}
                    </span>
                  )}
                </span>
              );
            })}
          </div>
        </div>

        {/* Event Timeline */}
        {flow.events.length > 0 && (
          <div className="mt-4 rounded-xl border border-gray-800 bg-gray-900 p-5">
            <h3 className="mb-3 text-sm font-semibold text-gray-300">Event Timeline</h3>
            <div className="max-h-64 overflow-y-auto">
              {flow.events.map((ev, i) => (
                <TimelineEntry key={i} event={ev} />
              ))}
              <div ref={timelineEndRef} />
            </div>
          </div>
        )}

        {/* Legend */}
        <div className="mt-6 flex flex-wrap justify-center gap-4 text-xs text-gray-500">
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-gray-600" /> Idle
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-blue-500" /> Active
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-green-500" /> Done
          </span>
          <span className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-red-500" /> Error
          </span>
          <span className="flex items-center gap-1.5">
            <span className="text-amber-500">(if)</span> conditional agent
          </span>
        </div>

        <p className="mt-8 text-center text-xs text-gray-600">
          Select a chat session above, then send a message from the Chat page
          to watch the agent flow animate in real time.
        </p>
      </div>
    </div>
  );
}
