"""CLI interface for apicost."""

import argparse
import sys
from apicost.costs import calculate_cost, estimate_cost, list_models


def format_currency(amount: float) -> str:
    """Format a dollar amount nicely."""
    if amount == 0:
        return "$0.00 (free)"
    if amount < 0.001:
        return f"${amount:.6f}"
    if amount < 0.01:
        return f"${amount:.4f}"
    return f"${amount:.2f}"


def cmd_calc(args: argparse.Namespace) -> None:
    """Calculate cost for given tokens."""
    result = calculate_cost(args.model, args.input_tokens, args.output_tokens)

    if "error" in result:
        print(f"\n  Error: {result['error']}\n")
        sys.exit(1)

    print(f"""
  Model:    {result['model']} ({result['provider']})
  Input:    {result['input_tokens']:,} tokens  ->  {format_currency(result['input_cost'])}
  Output:   {result['output_tokens']:,} tokens  ->  {format_currency(result['output_cost'])}
  ---------------------------------
  Total:    {format_currency(result['total_cost'])}
""")


def cmd_compare(args: argparse.Namespace) -> None:
    """Compare costs across all models."""
    input_tokens = args.input_tokens
    output_tokens = args.output_tokens

    print(f"\n  Cost comparison: {input_tokens:,} input + {output_tokens:,} output tokens\n")
    print(f"  {'Model':<25} {'Provider':<15} {'Input':<12} {'Output':<12} {'Total':<12}")
    print(f"  {'-' * 25} {'-' * 15} {'-' * 12} {'-' * 12} {'-' * 12}")

    results = []
    for model_info in list_models():
        result = calculate_cost(
            model_info["model"], input_tokens, output_tokens
        )
        if "error" not in result:
            results.append(result)

    # Sort by total cost
    results.sort(key=lambda x: x["total_cost"])

    for r in results:
        print(
            f"  {r['model']:<25} {r['provider']:<15} "
            f"{format_currency(r['input_cost']):<12} "
            f"{format_currency(r['output_cost']):<12} "
            f"{format_currency(r['total_cost']):<12}"
        )

    print()


def cmd_list(args: argparse.Namespace) -> None:
    """List all models with pricing."""
    print(f"\n  {'Model':<25} {'Provider':<15} {'Input/1M':<12} {'Output/1M':<12}")
    print(f"  {'-' * 25} {'-' * 15} {'-' * 12} {'-' * 12}")

    models = list_models()
    for m in models:
        print(
            f"  {m['model']:<25} {m['provider']:<15} "
            f"${m['input_per_1m']:<11.3f} ${m['output_per_1m']:<11.3f}"
        )

    print(f"\n  {len(models)} models listed.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="apicost",
        description="Know your AI API costs before you spend.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # calc command
    calc_parser = subparsers.add_parser("calc", help="Calculate cost for a model")
    calc_parser.add_argument("model", help="Model name (e.g., gpt-4o, claude-sonnet-4-6)")
    calc_parser.add_argument("-i", "--input-tokens", type=int, default=1000, help="Input tokens (default: 1000)")
    calc_parser.add_argument("-o", "--output-tokens", type=int, default=500, help="Output tokens (default: 500)")

    # compare command
    compare_parser = subparsers.add_parser("compare", help="Compare costs across all models")
    compare_parser.add_argument("-i", "--input-tokens", type=int, default=1000, help="Input tokens (default: 1000)")
    compare_parser.add_argument("-o", "--output-tokens", type=int, default=500, help="Output tokens (default: 500)")

    # list command
    subparsers.add_parser("list", help="List all models and pricing")

    args = parser.parse_args()

    if args.command == "calc":
        cmd_calc(args)
    elif args.command == "compare":
        cmd_compare(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
