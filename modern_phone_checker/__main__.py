# modern_phone_checker/__main__.py
"""Command-line interface with enhanced display and mock monetization."""

import asyncio
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime

from .core import PhoneChecker
from .email_checker import EmailChecker
from .cache import CacheManager
from .platforms import DEFAULT_PLATFORMS
from .utils import validate_phone_number

console = Console()

FREE_PHONE_PLATFORMS = ["whatsapp", "telegram"]

def format_timestamp(timestamp: datetime) -> str:
    """Format a datetime into a readable string."""
    return timestamp.strftime("%H:%M:%S %d/%m/%Y")


def create_result_table(results):
    """Create a rich table to display results."""
    table = Table(box=box.ROUNDED)
    table.add_column("Platform", style="cyan bold")
    table.add_column("Status", style="green bold")
    table.add_column("Details", style="yellow")
    table.add_column("Checked At", style="blue")

    for result in results:
        status = "[green]✓ Found[/green]" if getattr(result, "exists", False) else "[red]✗ Not Found[/red]"
        details = []
        if getattr(result, "error", None):
            details.append(f"Error: {result.error}")
        if getattr(result, "username", None):
            details.append(f"Username: {result.username}")
        if getattr(result, "metadata", None):
            for key, value in result.metadata.items():
                details.append(f"{key}: {value}")
        details_text = "\n".join(details) if details else "-"
        checked_at = format_timestamp(result.timestamp)
        table.add_row(result.platform.upper(), status, details_text, checked_at)

    return table


@click.group()
def cli():
    """Modern Phone Checker CLI."""
    pass


@cli.command()
@click.option("--phone", help="Phone number in E.164 format (e.g., +5511999998888).", default=None)
@click.option("--email", help="Email address to check (e.g., example@domain.com).", default=None)
@click.option("--api-key", "api_key", help="API key to enable premium features.", default=None)
@click.option("--country", "-c", help="Country code (default: 33 for France).", default="33")
@click.option("--force-refresh", is_flag=True, help="Ignore cache and force a fresh verification.")
@click.option("--cache-expire", "cache_expire", type=int, default=3600, show_default=True,
              help="Cache expiration time in seconds.")
def check(phone, email, api_key, country, force_refresh, cache_expire):
    """
    Check a phone number or an email address across platforms.
    """

    async def run():
        # 1) Input validation
        if phone and not validate_phone_number(phone, country):
            console.print(Panel(f"[red]Invalid phone number:[/] {phone}", title="Validation Error", border_style="red"))
            return
        if not phone and not email:
            console.print("[red]Error: please provide --phone or --email[/]")
            raise click.UsageError("Use --phone or --email")

        # 2) Decide which phone platforms to run
        phone_platforms = FREE_PHONE_PLATFORMS if not api_key else DEFAULT_PLATFORMS

        # 3) Initialize cache
        cache = CacheManager(expire_after=cache_expire)

        results = []
        with console.status("[bold blue]Checking in progress..."):
            # 4) Phone checks
            if phone:
                phone_checker = PhoneChecker(api_key=api_key, cache=cache, platforms=phone_platforms)
                results.extend(await phone_checker.check_number(phone, country, force_refresh=force_refresh))
                await phone_checker.close()

            # 5) Email check (premium only)
            if email:
                if not api_key:
                    console.print("[yellow]Skipping email check; --api-key required for email verification.[/]")
                else:
                    email_checker = EmailChecker(api_key=api_key, cache=cache)
                    results.append(email_checker.check(email))

        # 6) Display
        console.print("\n")
        target = phone if phone else email
        console.print(Panel(f"Results for: [bold]{target}[/bold]", style="cyan"))
        console.print(create_result_table(results))

    asyncio.run(run())


if __name__ == "__main__":
    cli()
