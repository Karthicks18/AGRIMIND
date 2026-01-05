import subprocess

def run_llama(prompt: str) -> str:
    try:
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            errors="ignore"
        )

        output, _ = process.communicate(prompt, timeout=120)
        return output.strip()

    except Exception as e:
        return f"Error running LLaMA: {e}"
