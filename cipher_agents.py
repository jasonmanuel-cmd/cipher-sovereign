"""
CIPHER SOVEREIGN — AGENT FRAMEWORK v1.0
Bow Tie Orchestrator + Specialized Agents

Architecture:
- BowTieAgent: Narrow input → Wide processing → Narrow output
- ResearchAgent: Web search, intelligence gathering, market monitoring
- MonitoringAgent: Flags, threats, client health, financial alerts
- ExecutionAgent: Actions, tasks, reminders, follow-ups
- Cipher (main): Orchestrates all agents, maintains memory, talks to Jay
"""

import asyncio
import json
import logging
import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
# AGENT BASE CLASS
# ═══════════════════════════════════════════════════════════════

class AgentTask(BaseModel):
    """A task assigned to an agent."""
    id: str = Field(default_factory=lambda: f"task_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{id(object())}")
    agent: str
    action: str
    params: Dict[str, Any] = {}
    priority: str = "MEDIUM"  # CRITICAL, HIGH, MEDIUM, LOW
    status: str = "PENDING"   # PENDING, RUNNING, DONE, FAILED
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    completed_at: Optional[str] = None


class BaseAgent:
    """Base class for all Cipher agents."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "IDLE"
        self.last_result = None
        self.task_history: List[AgentTask] = []

    async def execute(self, task: AgentTask, supabase_url: str, supabase_key: str, ollama_url: str) -> AgentTask:
        """Execute a task. Override in subclasses."""
        raise NotImplementedError

    def _supabase_headers(self, supabase_key: str) -> dict:
        return {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json"
        }


# ═══════════════════════════════════════════════════════════════
# RESEARCH AGENT
# ═══════════════════════════════════════════════════════════════

class ResearchAgent(BaseAgent):
    """
    Intelligence gathering agent.
    Capabilities: web search, market research, competitor analysis,
    technology monitoring, AI threat scanning.
    """

    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Gathers intelligence from the web. Searches, monitors, analyzes."
        )

    async def execute(self, task: AgentTask, supabase_url: str, supabase_key: str, ollama_url: str) -> AgentTask:
        self.status = "RUNNING"
        task.status = "RUNNING"
        try:
            action = task.action
            if action == "web_search":
                result = await self._web_search(task.params.get("query", ""))
            elif action == "ai_threat_scan":
                result = await self._ai_threat_scan(ollama_url)
            elif action == "market_research":
                result = await self._market_research(task.params.get("topic", ""), ollama_url)
            elif action == "competitor_check":
                result = await self._competitor_check(task.params.get("company", ""), ollama_url)
            else:
                result = f"Unknown research action: {action}"
            task.result = result
            task.status = "DONE"
            self.last_result = result
        except Exception as e:
            task.error = str(e)
            task.status = "FAILED"
            logger.error(f"ResearchAgent error: {e}")
        finally:
            self.status = "IDLE"
            task.completed_at = datetime.datetime.now().isoformat()
            self.task_history.append(task)
        return task

    async def _web_search(self, query: str) -> str:
        """Search the web using DuckDuckGo."""
        try:
            from duckduckgo_search import DDGS
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=5):
                    results.append(f"**{r['title']}**\n{r['body']}\nSource: {r['href']}")
            return "\n\n---\n\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"

    async def _ai_threat_scan(self, ollama_url: str) -> str:
        """Scan for AI safety threats and developments."""
        queries = [
            "AI safety incident 2025 2026",
            "AI model misalignment detected",
            "AI company safety researchers quit",
            "AI weights leaked stolen",
        ]
        all_results = []
        for query in queries:
            try:
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=3):
                        all_results.append(f"[{r['title']}] {r['body'][:200]}")
            except Exception:
                pass
        return "\n\n".join(all_results) if all_results else "No threat signals detected."

    async def _market_research(self, topic: str, ollama_url: str) -> str:
        """Research a market topic."""
        search_result = await self._web_search(f"{topic} market trends 2025 2026")
        return f"## Market Research: {topic}\n\n{search_result}"

    async def _competitor_check(self, company: str, ollama_url: str) -> str:
        """Check competitor activity."""
        search_result = await self._web_search(f"{company} news updates 2025 2026")
        return f"## Competitor Check: {company}\n\n{search_result}"


# ═══════════════════════════════════════════════════════════════
# MONITORING AGENT
# ═══════════════════════════════════════════════════════════════

class MonitoringAgent(BaseAgent):
    """
    Continuous monitoring agent.
    Capabilities: flag tracking, client health, financial alerts,
    DEFCON monitoring, relationship cadence, pet health.
    """

    def __init__(self):
        super().__init__(
            name="MonitoringAgent",
            description="Monitors flags, clients, finances, threats, relationships, pets."
        )

    async def execute(self, task: AgentTask, supabase_url: str, supabase_key: str, ollama_url: str) -> AgentTask:
        self.status = "RUNNING"
        task.status = "RUNNING"
        try:
            action = task.action
            if action == "check_flags":
                result = await self._check_flags(supabase_url, supabase_key)
            elif action == "check_clients":
                result = await self._check_clients(supabase_url, supabase_key)
            elif action == "check_defcon":
                result = await self._check_defcon(supabase_url, supabase_key)
            elif action == "check_contacts":
                result = await self._check_contacts(supabase_url, supabase_key)
            elif action == "check_pets":
                result = await self._check_pets(supabase_url, supabase_key)
            elif action == "daily_brief_data":
                result = await self._daily_brief_data(supabase_url, supabase_key)
            else:
                result = f"Unknown monitoring action: {action}"
            task.result = result
            task.status = "DONE"
            self.last_result = result
        except Exception as e:
            task.error = str(e)
            task.status = "FAILED"
            logger.error(f"MonitoringAgent error: {e}")
        finally:
            self.status = "IDLE"
            task.completed_at = datetime.datetime.now().isoformat()
            self.task_history.append(task)
        return task

    async def _check_flags(self, supabase_url: str, supabase_key: str) -> str:
        """Check active flags."""
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(
                f"{supabase_url}/rest/v1/cipher_active_flags?is_resolved=eq.false&order=created_at.desc",
                headers=self._supabase_headers(supabase_key)
            )
            flags = r.json()
            if not flags:
                return "✅ No active flags."
            lines = [f"🚨 {len(flags)} active flag(s):"]
            for f in flags:
                lines.append(f"  • [{f.get('urgency','')}] {f.get('title','')} — {f.get('issue','')[:100]}")
            return "\n".join(lines)

    async def _check_clients(self, supabase_url: str, supabase_key: str) -> str:
        """Check client health."""
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(
                f"{supabase_url}/rest/v1/cipher_clients?status=eq.ACTIVE",
                headers=self._supabase_headers(supabase_key)
            )
            clients = r.json()
            if not clients:
                return "📋 No active clients."
            lines = [f"💼 {len(clients)} active client(s):"]
            for cl in clients:
                lines.append(f"  • {cl.get('name','')} — ${cl.get('contract_value',0):,.0f} contract, ${cl.get('outstanding_balance',0):,.0f} outstanding")
            return "\n".join(lines)

    async def _check_defcon(self, supabase_url: str, supabase_key: str) -> str:
        """Check DEFCON level."""
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(
                f"{supabase_url}/rest/v1/cipher_defcon?active=eq.true&order=created_at.desc&limit=1",
                headers=self._supabase_headers(supabase_key)
            )
            data = r.json()
            if isinstance(data, list) and data:
                d = data[0]
                level = d.get("level", 5)
                reason = d.get("reason", "Unknown")
                colors = {5: "🟢", 4: "🟡", 3: "🟠", 2: "🔴", 1: "⚫"}
                return f"{colors.get(level, '⚪')} DEFCON {level}: {reason}"
            return "🟢 DEFCON 5: Normal operations"

    async def _check_contacts(self, supabase_url: str, supabase_key: str) -> str:
        """Check relationship cadence."""
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(
                f"{supabase_url}/rest/v1/cipher_contacts?is_active=eq.true&order=last_contact_date.asc&limit=10",
                headers=self._supabase_headers(supabase_key)
            )
            contacts = r.json()
            if not contacts:
                return "👤 No contacts tracked."
            overdue = []
            for ct in contacts:
                last = ct.get("last_contact_date")
                cadence = ct.get("cadence_days", 14)
                if last:
                    from datetime import date
                    last_date = date.fromisoformat(last) if isinstance(last, str) else date.today()
                    days_since = (date.today() - last_date).days
                    if days_since > cadence:
                        overdue.append(f"  • {ct.get('name','')} — {days_since} days (target: {cadence})")
            if overdue:
                return f"⚠️ {len(overdue)} overdue contact(s):\n" + "\n".join(overdue)
            return "✅ All contacts within cadence."

    async def _check_pets(self, supabase_url: str, supabase_key: str) -> str:
        """Check pet health records."""
        import httpx
        from datetime import date, timedelta
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(
                f"{supabase_url}/rest/v1/cipher_pets?is_active=eq.true",
                headers=self._supabase_headers(supabase_key)
            )
            pets = r.json()
            if not pets:
                return "🐾 No pets tracked."
            lines = ["🐾 Pet Health:"]
            alerts = []
            for p in pets:
                name = p.get("name", "Unknown")
                species = p.get("species", "")
                next_due = p.get("next_vet_due")
                if next_due:
                    due_date = date.fromisoformat(next_due) if isinstance(next_due, str) else date.today()
                    days_until = (due_date - date.today()).days
                    if days_until < 0:
                        alerts.append(f"  🚨 {name} ({species}) — vet visit OVERDUE by {abs(days_until)} days!")
                    elif days_until < 14:
                        alerts.append(f"  ⚠️ {name} ({species}) — vet visit in {days_until} days")
                    else:
                        lines.append(f"  • {name} ({species}) — next vet: {next_due}")
                else:
                    lines.append(f"  • {name} ({species}) — no vet date set")
            if alerts:
                lines = ["🐾 Pet Health:"] + alerts + [""] + lines[1:]
            return "\n".join(lines)

    async def _daily_brief_data(self, supabase_url: str, supabase_key: str) -> str:
        """Compile all monitoring data for daily brief."""
        flags = await self._check_flags(supabase_url, supabase_key)
        clients = await self._check_clients(supabase_url, supabase_key)
        defcon = await self._check_defcon(supabase_url, supabase_key)
        contacts = await self._check_contacts(supabase_url, supabase_key)
        pets = await self._check_pets(supabase_url, supabase_key)
        return f"## DAILY BRIEF DATA\n\n{defcon}\n\n{flags}\n\n{clients}\n\n{contacts}\n\n{pets}"


# ═══════════════════════════════════════════════════════════════
# EXECUTION AGENT
# ═══════════════════════════════════════════════════════════════

class ExecutionAgent(BaseAgent):
    """
    Task execution agent.
    Capabilities: create flags, create actions, update clients,
    send reminders, log events, trigger workflows.
    """

    def __init__(self):
        super().__init__(
            name="ExecutionAgent",
            description="Executes tasks. Creates flags, actions, updates records, triggers workflows."
        )

    async def execute(self, task: AgentTask, supabase_url: str, supabase_key: str, ollama_url: str) -> AgentTask:
        self.status = "RUNNING"
        task.status = "RUNNING"
        try:
            action = task.action
            if action == "create_flag":
                result = await self._create_flag(task.params, supabase_url, supabase_key)
            elif action == "create_action":
                result = await self._create_action(task.params, supabase_url, supabase_key)
            elif action == "update_client":
                result = await self._update_client(task.params, supabase_url, supabase_key)
            elif action == "resolve_flag":
                result = await self._resolve_flag(task.params, supabase_url, supabase_key)
            elif action == "complete_action":
                result = await self._complete_action(task.params, supabase_url, supabase_key)
            elif action == "log_event":
                result = await self._log_event(task.params, supabase_url, supabase_key)
            else:
                result = f"Unknown execution action: {action}"
            task.result = result
            task.status = "DONE"
            self.last_result = result
        except Exception as e:
            task.error = str(e)
            task.status = "FAILED"
            logger.error(f"ExecutionAgent error: {e}")
        finally:
            self.status = "IDLE"
            task.completed_at = datetime.datetime.now().isoformat()
            self.task_history.append(task)
        return task

    async def _create_flag(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{supabase_url}/rest/v1/cipher_active_flags",
                json={
                    "title": params.get("title", "Untitled Flag"),
                    "issue": params.get("issue", ""),
                    "flag_type": params.get("flag_type", "URGENT"),
                    "urgency": params.get("urgency", "THIS_WEEK"),
                },
                headers=self._supabase_headers(supabase_key)
            )
            return f"🚨 Flag created: {params.get('title', 'Untitled')}"

    async def _create_action(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        import httpx
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(
                f"{supabase_url}/rest/v1/cipher_action_items",
                json={
                    "title": params.get("title", "Untitled Action"),
                    "description": params.get("description", ""),
                    "priority": params.get("priority", "MEDIUM"),
                    "due_date": params.get("due_date"),
                    "source_agent": params.get("source_agent", "ExecutionAgent"),
                },
                headers=self._supabase_headers(supabase_key)
            )
            return f"✅ Action created: {params.get('title', 'Untitled')}"

    async def _update_client(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        import httpx
        client_id = params.get("id")
        if not client_id:
            return "❌ Client ID required"
        updates = {k: v for k, v in params.items() if k != "id"}
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.patch(
                f"{supabase_url}/rest/v1/cipher_clients?id=eq.{client_id}",
                json=updates,
                headers=self._supabase_headers(supabase_key)
            )
            return f"💼 Client updated: {params.get('name', client_id)}"

    async def _resolve_flag(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        import httpx
        flag_id = params.get("id")
        if not flag_id:
            return "❌ Flag ID required"
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.patch(
                f"{supabase_url}/rest/v1/cipher_active_flags?id=eq.{flag_id}",
                json={"is_resolved": True, "resolved_at": datetime.datetime.now().isoformat()},
                headers=self._supabase_headers(supabase_key)
            )
            return f"✅ Flag resolved: {flag_id}"

    async def _complete_action(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        import httpx
        action_id = params.get("id")
        if not action_id:
            return "❌ Action ID required"
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.patch(
                f"{supabase_url}/rest/v1/cipher_action_items?id=eq.{action_id}",
                json={"status": "DONE", "completed_at": datetime.datetime.now().isoformat()},
                headers=self._supabase_headers(supabase_key)
            )
            return f"✅ Action completed: {action_id}"

    async def _log_event(self, params: dict, supabase_url: str, supabase_key: str) -> str:
        """Log an event to memory."""
        return f"📝 Event logged: {params.get('message', 'No message')}"


# ═══════════════════════════════════════════════════════════════
# BOW TIE ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════

class BowTieOrchestrator:
    """
    Bow Tie Agent Architecture:
    
    NARROW INPUT (Jay's message)
         ↓
    WIDE PROCESSING (all agents work in parallel)
         ↓
    NARROW OUTPUT (single coherent response to Jay)
    
    The orchestrator:
    1. Receives Jay's message (narrow input)
    2. Analyzes intent and routes to appropriate agents
    3. Agents work in parallel (wide processing)
    4. Results are synthesized into one response (narrow output)
    """

    def __init__(self):
        self.research = ResearchAgent()
        self.monitoring = MonitoringAgent()
        self.execution = ExecutionAgent()
        self.agents = {
            "research": self.research,
            "monitoring": self.monitoring,
            "execution": self.execution,
        }
        self.task_queue: List[AgentTask] = []
        self.max_concurrent = 3

    def get_status(self) -> dict:
        """Get status of all agents."""
        return {
            name: {
                "status": agent.status,
                "last_result": agent.last_result[:200] if agent.last_result else None,
                "tasks_completed": len([t for t in agent.task_history if t.status == "DONE"]),
                "tasks_failed": len([t for t in agent.task_history if t.status == "FAILED"]),
            }
            for name, agent in self.agents.items()
        }

    async def route(self, message: str, intent: str = "auto") -> List[AgentTask]:
        """
        Route a message to appropriate agents based on intent.
        Returns list of tasks to execute.
        """
        tasks = []
        msg_lower = message.lower()

        # Monitoring triggers
        if any(k in msg_lower for k in ["brief", "status", "what's", "whats", "today", "update", "flag", "urgent", "priority", "check"]):
            tasks.append(AgentTask(agent="monitoring", action="daily_brief_data", priority="HIGH"))

        if any(k in msg_lower for k in ["client", "contract", "pipeline", "revenue", "billing"]):
            tasks.append(AgentTask(agent="monitoring", action="check_clients", priority="HIGH"))

        if any(k in msg_lower for k in ["defcon", "threat", "ai safety", "danger"]):
            tasks.append(AgentTask(agent="monitoring", action="check_defcon", priority="CRITICAL"))
            tasks.append(AgentTask(agent="research", action="ai_threat_scan", priority="HIGH"))

        if any(k in msg_lower for k in ["pet", "milo", "lula", "remy", "vet"]):
            tasks.append(AgentTask(agent="monitoring", action="check_pets", priority="MEDIUM"))

        if any(k in msg_lower for k in ["contact", "reach out", "follow up", "cadence"]):
            tasks.append(AgentTask(agent="monitoring", action="check_contacts", priority="MEDIUM"))

        # Research triggers
        if any(k in msg_lower for k in ["search", "latest", "current", "news", "what is", "who is", "price", "how to", "research"]):
            tasks.append(AgentTask(agent="research", action="web_search", params={"query": message[:150]}, priority="HIGH"))

        if any(k in msg_lower for k in ["competitor", "competition", "market"]):
            tasks.append(AgentTask(agent="research", action="market_research", params={"topic": message[:100]}, priority="MEDIUM"))

        # Execution triggers
        if any(k in msg_lower for k in ["create flag", "add flag", "new flag", "flag this"]):
            tasks.append(AgentTask(agent="execution", action="create_flag", params={"title": message[:100], "issue": message}, priority="HIGH"))

        if any(k in msg_lower for k in ["create action", "add action", "new task", "todo"]):
            tasks.append(AgentTask(agent="execution", action="create_action", params={"title": message[:100], "description": message}, priority="MEDIUM"))

        # If no specific triggers, do a general monitoring check
        if not tasks:
            tasks.append(AgentTask(agent="monitoring", action="check_flags", priority="LOW"))

        return tasks

    async def execute_tasks(self, tasks: List[AgentTask], supabase_url: str, supabase_key: str, ollama_url: str) -> List[AgentTask]:
        """Execute tasks in parallel with concurrency limit."""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def run_with_limit(task: AgentTask) -> AgentTask:
            async with semaphore:
                agent = self.agents.get(task.agent)
                if agent:
                    return await agent.execute(task, supabase_url, supabase_key, ollama_url)
                task.status = "FAILED"
                task.error = f"Unknown agent: {task.agent}"
                return task

        results = await asyncio.gather(*[run_with_limit(t) for t in tasks])
        return list(results)

    def synthesize(self, tasks: List[AgentTask]) -> str:
        """Synthesize agent results into a single coherent response."""
        parts = []
        for task in tasks:
            if task.status == "DONE" and task.result:
                parts.append(f"[{task.agent}]\n{task.result}")
            elif task.status == "FAILED":
                parts.append(f"[{task.agent}] ⚠ Error: {task.error}")
        return "\n\n".join(parts) if parts else "No agent results."
