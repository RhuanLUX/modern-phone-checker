"""Command-line interface with enhanced display."""

import asyncio
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
from . import PhoneChecker
from .utils import validate_phone_number

console = Console()

def format_timestamp(timestamp):
    """Format the timestamp into a readable string."""
    return timestamp.strftime("%H:%M:%S %d/%m/%Y")

def create_result_table(results):
    """Create a rich table to display results."""
    table = Table(box=box.ROUNDED)
    table.add_column("Platform", style="cyan bold")
    table.add_column("Status", style="green bold")
    table.add_column("Details", style="yellow")
    table.add_column("Checked At", style="blue")

    for result in results:
        status = "[green]✓ Found[/green]" if result.exists else "[red]✗ Not Found[/red]"
        details = []

        if result.error:
            details.append(f"Error: {result.error}")
        if result.username:
            details.append(f"Username: {result.username}")
        if result.metadata:
            for key, value in result.metadata.items():
                details.append(f"{key}: {value}")

        details_text = "\n".join(details) if details else "-"
        timestamp = format_timestamp(result.timestamp)

        table.add_row(
            result.platform.upper(),
            status,
            details_text,
            timestamp
        )

    return table

@click.group()
def cli():
    """Modern Phone Checker CLI"""
    pass

@cli.command()
@click.argument('phone')
@click.option('--country', '-c', default='33', help='Country code (default: 33 for France)')
@click.option('--force-refresh', is_flag=True, help='Ignore cache and force a new verification.')
def check(phone: str, country: str, force_refresh: bool):
    """Check a phone number across different platforms."""

    async def run():
        if not validate_phone_number(phone, country):
            console.print(Panel(
                "[red]Invalid phone number format![/red]\n\n"
                f"The number {phone} does not seem valid for country code {country}.",
                title="Validation Error",
                border_style="red"
            ))
            return

        with console.status("[bold blue]Checking in progress..."):
            checker = PhoneChecker()
            try:
                results = await checker.check_number(phone, country, force_refresh=force_refresh)
                console.print("\n")
                console.print(Panel(
                    f"Results for number: [bold]+{country} {phone}[/bold]",
                    style="cyan"
                ))
                console.print(create_result_table(results))
            finally:
                await checker.close()

    asyncio.run(run())

if __name__ == '__main__':
    cli()
