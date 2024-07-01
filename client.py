import argparse
import requests


def main():
    parser = argparse.ArgumentParser(
        description="Submit LaTeX fragments to the server for compilation and conversion to SVG."
    )
    parser.add_argument(
        "fragment_file",
        type=str,
        help="Path to the file containing the LaTeX fragment.",
    )
    parser.add_argument(
        "-p",
        "--preamble_file",
        type=str,
        help="Path to the file containing additional LaTeX preamble (optional).",
    )
    parser.add_argument(
        "-o", "--output", type=str, default="output.svg", help="Output SVG file name."
    )
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:5000/compile",
        help="URL of the LaTeX compilation server.",
    )

    args = parser.parse_args()

    # Read LaTeX fragment
    with open(args.fragment_file, "r") as file:
        fragment = file.read()

    # Read preamble if provided
    preamble = ""
    if args.preamble_file:
        with open(args.preamble_file, "r") as file:
            preamble = file.read()

    # Prepare the payload
    payload = {"fragment": fragment, "preamble": preamble}

    # Send POST request to the server
    response = requests.post(args.url, json=payload)

    if response.status_code == 200:
        with open(args.output, "wb") as file:
            file.write(response.content)
        print(f"Output SVG saved to {args.output}")
    else:
        print(f"Error: {response.status_code} - {response.json()}")


if __name__ == "__main__":
    main()
