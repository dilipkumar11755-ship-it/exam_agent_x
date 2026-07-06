import os
import sys
import re
from google import genai
from google.genai import types

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def clean_text(text: str) -> str:
    """Completely scrubs markdown characters like *, #, _, and ` for a pristine CLI appearance."""
    cleaned = re.sub(r'[\*\#\_`]', '', text)
    return cleaned.strip()

def format_headings(text: str) -> Text:
    """Scans text line-by-line and applies beautiful colors to structure the layout."""
    formatted_lines = []
    lines = text.split('\n')
    
    for line in lines:
        cleaned = clean_text(line)
        if not cleaned:
            formatted_lines.append(Text(""))
            continue
            
        if any(marker in cleaned.upper() for marker in ["DAY", "PERIOD", "TONIGHT", "WEEK"]):
            formatted_lines.append(Text(f"✨ {cleaned.upper()}", style="bold yellow underline"))
        elif "CORE TOPIC" in cleaned.upper() or "TOPICS TO MASTER" in cleaned.upper():
            formatted_lines.append(Text(f"🎯 {cleaned}", style="bold cyan"))
        elif "KEY CONCEPTS" in cleaned.upper() or "FORMULAS" in cleaned.upper():
            formatted_lines.append(Text(f"💡 {cleaned}", style="bold green"))
        elif "EXPECTED EXAM GOALS" in cleaned.upper() or "TARGET GOAL" in cleaned.upper():
            formatted_lines.append(Text(f"🏁 {cleaned}", style="bold magenta"))
        else:
            formatted_lines.append(Text(f"  {cleaned}", style="white"))
            
    combined_text = Text()
    for i, line_text in enumerate(formatted_lines):
        combined_text.append(line_text)
        if i < len(formatted_lines) - 1:
            combined_text.append("\n")
    return combined_text

def run_study_concierge():
    try:
        client = genai.Client()
    except Exception as e:
        console.print(f"[bold red]Initialization Error:[/] Ensure GEMINI_API_KEY is set. Details: {e}")
        return
    
    console.print("\n" * 2)
    console.print(Panel(
        "[bold cyan]🚀 EXAM AGENT X: PERSONAL STUDY DASHBOARD[/bold cyan]",
        border_style="cyan", expand=True
    ))
    
    user_syllabus = console.input("\n[bold yellow]➔ Enter your syllabus or topics to prepare:[/] ")
    if not user_syllabus.strip():
        user_syllabus = "Ai agents, multi-agent frameworks, human-in-the-loop systems"
        
    user_days = console.input("[bold yellow]➔ Enter your preparation timeline:[/] ")
    if not user_days.strip():
        user_days = "3 days"

    # -------------------------------------------------------------
    # STEP 1: STUDY PLAN GENERATION
    # -------------------------------------------------------------
    print("")
    with console.status("[bold green]Generating your study timeline...", spinner="dots"):
        planner_instructions = (
            "You are an expert academic planner. Divide the syllabus into the requested timeline. "
            "Do NOT use markdown syntax (no asterisks, hashtags). Use capital letters for headings. "
            "Provide details on Core Topics, Key Concepts/Formulas, and Expected Exam Goals."
        )
        try:
            planner_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Create a descriptive study timeline for '{user_days}' covering this syllabus:\n{user_syllabus}",
                config=types.GenerateContentConfig(system_instruction=planner_instructions)
            )
            raw_plan = planner_response.text
        except Exception as e:
            console.print(f"[bold red]Error generating plan:[/] {e}")
            return

    # Display Timeline Output
    console.print("\n[bold green]✔ Study plan generated successfully![/bold green]\n")
    styled_plan = format_headings(raw_plan)
    console.print(Panel(
        styled_plan,
        title="📆 YOUR DETAILED STUDY TIMELINE",
        border_style="green",
        padding=(1, 2),
        expand=True
    ))

    # -------------------------------------------------------------
    # STEP 2: INTERACTIVE MENU FOR ADDITIONAL FEATURES
    # -------------------------------------------------------------
    console.print("\n" + "─" * 60)
    console.print("[bold cyan]Would you like to prepare any additional study aids?[/bold cyan]")
    console.print("  [1] Attempt a Mock Viva Quiz")
    console.print("  [2] Generate Interactive Flashcards")
    console.print("  [3] Generate a Concise Topic Summary")
    console.print("  [4] No thanks, exit script")
    console.print("\n[bold green]💡 NOTE: You can select multiple options by separating them with commas (e.g., 1,2 or 1,2,3)[/bold green]")
    
    user_input = console.input("\n[bold yellow]➔ Select option(s): [/]").strip()
    console.print("─" * 60 + "\n")

    choices = [c.strip() for c in user_input.split(',')]

    for choice in choices:
        if choice not in ['1', '2', '3']:
            continue
            
        if choice == '1':
            task_prompt = "Draft exactly 3 high-yield conceptual short-answer viva questions based on the core topics."
            system_ins = "You are an expert academic examiner. Create 3 distinct question lines. Do not include answers, instructions, or markdown * or #."
            panel_title = "📝 CUSTOM MOCK VIVA PREPARATION QUESTIONS"
            
            with console.status("[bold magenta]Processing selection [1]...", spinner="dots"):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Using this plan, execute this task: {task_prompt}\n\nPlan:\n{raw_plan}",
                        config=types.GenerateContentConfig(system_instruction=system_ins)
                    )
                    clean_output = "\n".join([f"  {clean_text(line)}" for line in response.text.split('\n')])
                    console.print(Panel(Text(clean_output, style="white"), title=panel_title, border_style="magenta", padding=(1, 2), expand=True))
                except Exception as e:
                    console.print(f"[bold red]Error:[/] {e}")

        elif choice == '2':
            task_prompt = "Generate exactly 3 interactive flashcards. For each card, write 'FRONT:' followed by a key core term or concept, then on the next line write 'BACK:' followed by a clear, one-sentence explanation. Do not add any other layout characters."
            system_ins = "You are an expert flashcard indexer. Provide exactly 3 pairs of FRONT: and BACK: lines. No intro text, no conversational remarks, no markdown characters."
            
            with console.status("[bold magenta]Processing selection [2]...", spinner="dots"):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Using this plan, execute this task: {task_prompt}\n\nPlan:\n{raw_plan}",
                        config=types.GenerateContentConfig(system_instruction=system_ins)
                    )
                    raw_flash_data = response.text
                except Exception as e:
                    console.print(f"[bold red]Error:[/] {e}")
                    continue

            console.print("\n[bold yellow]🎴 INTERACTIVE FLASHCARD SESSION STARTING...[/bold yellow]")
            
            cards = re.findall(r'FRONT:\s*(.*?)\s*BACK:\s*(.*?)(?=FRONT:|$)', raw_flash_data, re.DOTALL | re.IGNORECASE)
            
            if not cards:
                lines = [clean_text(l) for l in raw_flash_data.split('\n') if l.strip()]
                cards = []
                for i in range(0, len(lines)-1, 2):
                    cards.append((lines[i], lines[i+1]))

            for idx, (front, back) in enumerate(cards[:3], 1):
                console.print(f"\n[bold cyan]Card {idx} of {min(len(cards), 3)}[/bold cyan]")
                
                # Render Card Front
                console.print(Panel(
                    Text(f"\n❓ {front.strip()}\n", style="bold white", justify="center"),
                    title="🎴 FLASHCARD FRONT", border_style="yellow", width=60
                ))
                
                # Wait for User Flip Input
                console.input("[dim white]➔ Press ENTER to flip card and reveal answer...[/dim white]")
                
                # Render Card Back
                console.print(Panel(
                    Text(f"\n💡 {back.strip()}\n", style="bold green", justify="center"),
                    title="🔄 FLASHCARD BACK (FLIPPED)", border_style="green", width=60
                ))

        elif choice == '3':
            task_prompt = "Create a condensed, high-level paragraph summary of the entire revision plan emphasizing core takeaways."
            system_ins = "You are an expert technical writer. Provide a tight, direct summary paragraph. Do not use markdown * or #."
            panel_title = "📋 CONCISE TOPIC REVISION SUMMARY"
            
            with console.status("[bold magenta]Processing selection [3]...", spinner="dots"):
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Using this plan, execute this task: {task_prompt}\n\nPlan:\n{raw_plan}",
                        config=types.GenerateContentConfig(system_instruction=system_ins)
                    )
                    clean_output = "\n".join([f"  {clean_text(line)}" for line in response.text.split('\n')])
                    console.print(Panel(Text(clean_output, style="white"), title=panel_title, border_style="cyan", padding=(1, 2), expand=True))
                except Exception as e:
                    console.print(f"[bold red]Error:[/] {e}")

        console.print("")

    console.print("[bold cyan]All requested targets generated. Best of luck with your preparation![/bold cyan]\n")

if __name__ == "__main__":
    run_study_concierge()
