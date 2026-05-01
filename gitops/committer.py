"""
Git-Ops Committer Agent (Agent #16)
Auto-commits and pushes with unhinged college-student commit messages.
"""

import subprocess
import random
import os
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 40+ commit message templates — sleep-deprived college student vibes
COMMIT_MESSAGES = [
    "initial commit. let's cook 🧑‍🍳",
    "fixed the options parser. i need a coffee.",
    "idek what this bug was but stackoverflow said do this",
    "added insider trading agent. SEC plz don't come for me",
    "frontend is looking sleek. defense is leakier than chelsea's backline rn but we push",
    "combinatorics optimization agent goes brrrrrr",
    "bruh typo",
    "wip: trying to make the grand synthesizer stop hallucinating",
    "git push --force because I am the captain now",
    "3am code. no thoughts head empty",
    "this commit is brought to you by monster energy",
    "if this breaks i'm switching majors",
    "added {component}. it works. i don't know why. don't touch it.",
    "refactored {component}. it's beautiful. i'm crying.",
    "fixed a bug that shouldn't have existed in the first place",
    "the dark pool monitor is monitoring. we are so back.",
    "nancy pelosi's trades agent is live. god help us all.",
    "sentiment analysis says buy. my gut says sell. trusting the robots.",
    "kelly criterion says go all in. this is financial advice (it is not).",
    "the swarm is alive. skynet origin story right here.",
    "why did i make 16 agents. why.",
    "this code is held together by vibes and caffeine",
    "pushed at {time}. sleep is for the weak.",
    "the technical analyst is drawing more lines than my art class",
    "options flow agent detected unusual activity. probably nothing. probably everything.",
    "sector comparator comparing. that's literally all it does.",
    "geopolitical risk agent found a risk. shocking. absolutely shocking.",
    "macro agent says recession. macro agent always says recession.",
    "i just mass reviewed 200 lines of GPT-4o output what is my life",
    "frontend animations are buttery smooth. everything else is on fire.",
    "the risk matrix is giving bloomberg terminal energy",
    "gauge chart sweeping like a windshield wiper. aesthetic.",
    "websocket streaming works. i feel like a real engineer now.",
    "added error handling because prod doesn't care about my feelings",
    "this function is O(n²) and i simply do not care right now",
    "lgtm (i did not actually look)",
    "merge conflict resolved through sheer willpower",
    "updated deps. pray nothing breaks.",
    "the README is longer than some of my essays",
    "finally fixed the CORS issue. my nemesis.",
]

COMPONENT_NAMES = [
    "macro agent", "geopolitical agent", "market regime agent",
    "technical analyst", "options flow agent", "dark pool monitor",
    "fundamental agent", "sector comparator", "insider trading agent",
    "media sentiment agent", "social scraper", "risk optimizer",
    "grand synthesizer", "report generator", "frontend dashboard",
    "API endpoint", "websocket handler", "state graph",
]


def _get_random_message(context: str = None) -> str:
    """Generate a randomized commit message with template filling."""
    msg = random.choice(COMMIT_MESSAGES)

    # Fill in template variables
    if "{component}" in msg:
        component = context if context else random.choice(COMPONENT_NAMES)
        msg = msg.replace("{component}", component)
    if "{time}" in msg:
        msg = msg.replace("{time}", datetime.now().strftime("%I:%M %p"))

    return msg


def auto_commit(message: str = None, context: str = None) -> bool:
    """
    Stage all changes, commit with a message, and push to origin.

    Args:
        message: Override commit message. If None, generates a random one.
        context: Optional context for template filling (e.g., component name).

    Returns:
        True if commit+push succeeded, False otherwise.
    """
    try:
        # Check if there are changes to commit
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

        if not status.stdout.strip():
            print("[GitOps] Nothing to commit — working tree clean.")
            return False

        # Stage all changes
        subprocess.run(
            ["git", "add", "."],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )

        # Generate commit message
        commit_msg = message if message else _get_random_message(context)

        # Commit
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

        print(f"[GitOps] Committed: {commit_msg}")

        # Push to origin
        push_result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

        if push_result.returncode == 0:
            print("[GitOps] Pushed to origin/main ✓")
            return True
        else:
            # Try pushing to master if main fails
            push_result = subprocess.run(
                ["git", "push", "-u", "origin", "master"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            if push_result.returncode == 0:
                print("[GitOps] Pushed to origin/master ✓")
                return True
            else:
                print(f"[GitOps] Push failed: {push_result.stderr}")
                return False

    except subprocess.CalledProcessError as e:
        print(f"[GitOps] Error: {e}")
        return False
    except Exception as e:
        print(f"[GitOps] Unexpected error: {e}")
        return False


if __name__ == "__main__":
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    auto_commit(message=msg)
