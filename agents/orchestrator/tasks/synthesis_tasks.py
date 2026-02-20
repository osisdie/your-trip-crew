"""Task definitions for the Synthesis Crew."""

from crewai import Task


def create_synthesis_task(agent, state_summary: str) -> Task:
    return Task(
        description=(
            f"Assemble all gathered information into a complete, polished travel itinerary.\n\n"
            f"Available data:\n{state_summary}\n\n"
            f"Create a beautiful, comprehensive response that includes:\n"
            f"1. Trip overview (destination, dates, travelers)\n"
            f"2. Day-by-day itinerary with times and activities\n"
            f"3. Hotel recommendations for each city\n"
            f"4. Flight options\n"
            f"5. Transport plan (trains/passes)\n"
            f"6. Cost breakdown by category\n"
            f"7. Practical tips (eSIM, currency, packing)\n"
            f"8. Family advice (if applicable)\n\n"
            f"Format the output in clear, readable markdown. "
            f"Respond in the same language as the original user request."
        ),
        expected_output="Complete, polished travel itinerary in markdown format",
        agent=agent,
    )
