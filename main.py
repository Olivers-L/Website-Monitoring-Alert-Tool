import argparse
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()


def print_status(url, status, message):
    if status == "UP":
        console.print(f"[green]✔ UP[/green] {url} [dim]- {message}[/dim]")
    elif status == "DOWN":
        console.print(f"[red]✖ DOWN[/red] {url} [dim]- {message}[/dim]")
    elif status == "WARN":
        console.print(f"[yellow]⚠ WARN[/yellow] {url} [dim]- {message}[/dim]")


def check_website(url, max_response_time):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start

        if elapsed > max_response_time:
            print_status(
                url,
                "WARN",
                f"Slow response ({elapsed:.2f}s)"
            )
        else:
            print_status(
                url,
                "UP",
                f"{response.status_code} OK ({elapsed:.2f}s)"
            )

    except requests.exceptions.Timeout:
        print_status(url, "DOWN", "Request timed out")
    except requests.exceptions.ConnectionError:
        print_status(url, "DOWN", "DNS resolution failed")
    except Exception as e:
        print_status(url, "DOWN", str(e))


def main():
    parser = argparse.ArgumentParser(description="Website Monitoring Tool")
    parser.add_argument("url", help="Website URL to monitor")
    parser.add_argument("--interval", type=int, default=300, help="Check interval in seconds")
    parser.add_argument("--max-response-time", type=float, default=1.0, help="Max response time in seconds")

    args = parser.parse_args()

    console.print(
        Panel.fit(
            "[bold cyan]Website Monitoring Tool[/bold cyan]\n"
            "[dim]Press Ctrl+C to stop[/dim]",
            box=box.ROUNDED,
        )
    )

    console.print(
        f"[dim]Monitoring {args.url} every {args.interval}s[/dim]\n"
    )

    try:
        while True:
            check_website(args.url, args.max_response_time)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        console.print("\n[bold red]Monitoring stopped[/bold red]")


if __name__ == "__main__":
    main()
