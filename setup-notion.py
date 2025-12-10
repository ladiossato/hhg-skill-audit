#!/usr/bin/env python3
"""
HHG Skill Audit - Notion Database Setup Script

This script creates the Notion database with all required properties.
Run once before using the audit application.

Usage: python setup-notion.py
"""

import requests
import json
import sys

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

PARENT_PAGE_ID = "2c501ad84ed880e5a4edc56122f60cb7"

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════════════════

def log_enter(fn, params=None):
    print(f"[{fn}] > ENTER", f"| params: {params}" if params else "")

def log_exit(fn, result=None):
    print(f"[{fn}] OK EXIT", f"| result: {result}" if result else "")

def log_error(fn, err):
    print(f"[{fn}] X ERROR | {err}", file=sys.stderr)

def log_data(fn, label, data):
    print(f"[{fn}] DATA {label}: {data}")

def log_network(fn, method, url, status):
    symbol = "OK" if status < 400 else "X"
    print(f"[{fn}] NET {method} {symbol} | {url} | Status: {status}")

# ══════════════════════════════════════════════════════════════════════════════
# DATA (from SPEC.md)
# ══════════════════════════════════════════════════════════════════════════════

TEAM_MEMBER_OPTIONS = [
    {"name": "Lydell Tyler", "color": "blue"},
    {"name": "Efrain Campos", "color": "green"},
    {"name": "Ismael Costilla", "color": "yellow"},
    {"name": "Lizbeth Espinoza", "color": "pink"},
    {"name": "Anthony Esparza", "color": "purple"},
    {"name": "David Slavoff", "color": "orange"},
    {"name": "Refugio Guzman", "color": "red"},
    {"name": "Sarah Lopez", "color": "blue"},
    {"name": "Edgar Jaimes", "color": "green"},
    {"name": "David Crafton", "color": "yellow"},
    {"name": "Anthony Gonzalez", "color": "pink"},
    {"name": "Brittany Gomez", "color": "purple"},
    {"name": "Floyd Jefferson", "color": "orange"},
    {"name": "Erin Hirtzig", "color": "red"}
]

STATION_OPTIONS = [
    {"name": "Cook", "color": "red"},
    {"name": "Mid-pack", "color": "orange"},
    {"name": "Expo", "color": "green"},
    {"name": "Float", "color": "blue"}
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ══════════════════════════════════════════════════════════════════════════════

def create_database():
    """Create Notion database with all required properties."""
    log_enter("create_database")

    url = "https://api.notion.com/v1/databases"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    payload = {
        "parent": {
            "type": "page_id",
            "page_id": PARENT_PAGE_ID
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "HHG Skill Audit"
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Team Member": {
                "select": {
                    "options": TEAM_MEMBER_OPTIONS
                }
            },
            "Station": {
                "select": {
                    "options": STATION_OPTIONS
                }
            },
            "Date": {
                "date": {}
            },
            "Buffer": {
                "number": {
                    "format": "number"
                }
            },
            "Staging": {
                "number": {
                    "format": "number"
                }
            },
            "Docking": {
                "number": {
                    "format": "number"
                }
            },
            "Focus": {
                "number": {
                    "format": "number"
                }
            },
            "Total Orders": {
                "number": {
                    "format": "number"
                }
            },
            "Total Misses": {
                "number": {
                    "format": "number"
                }
            },
            "Miss Rate": {
                "number": {
                    "format": "percent"
                }
            }
        }
    }

    log_data("create_database", "Payload size", f"{len(json.dumps(payload))} bytes")
    log_data("create_database", "Team members", len(TEAM_MEMBER_OPTIONS))
    log_data("create_database", "Properties", list(payload["properties"].keys()))

    try:
        response = requests.post(url, headers=headers, json=payload)
        log_network("create_database", "POST", url, response.status_code)

        if response.status_code == 200:
            data = response.json()
            database_id = data["id"]
            database_url = data.get("url", "N/A")

            print("\n" + "=" * 70)
            print("SUCCESS! Database created.")
            print("=" * 70)
            print(f"Database ID: {database_id}")
            print(f"Database URL: {database_url}")
            print("=" * 70)
            print("\nUse this Database ID in your HTML application:")
            print(f"  {database_id.replace('-', '')}")
            print("=" * 70 + "\n")

            log_exit("create_database", {"id": database_id})
            return database_id
        else:
            error_data = response.json()
            log_error("create_database", f"Status {response.status_code}: {error_data}")

            print("\n" + "=" * 70)
            print("ERROR: Failed to create database")
            print("=" * 70)
            print(f"Status: {response.status_code}")
            print(f"Error: {json.dumps(error_data, indent=2)}")
            print("=" * 70 + "\n")

            # Common error handling
            if response.status_code == 401:
                print("HINT: Check that your Notion integration token is correct.")
            elif response.status_code == 404:
                print("HINT: Check that the parent page ID is correct and the integration has access to it.")
            elif response.status_code == 400:
                print("HINT: The parent page may need to be shared with your integration.")
                print("      Go to the Notion page -> Share -> Invite -> Select your integration")

            return None

    except requests.exceptions.RequestException as e:
        log_error("create_database", str(e))
        print(f"\nNetwork error: {e}")
        return None


def main():
    """Main entry point."""
    log_enter("main")

    print("\n" + "=" * 70)
    print("HHG SKILL AUDIT - NOTION DATABASE SETUP")
    print("=" * 70 + "\n")

    print(f"Parent Page ID: {PARENT_PAGE_ID}")
    print(f"Team Members: {len(TEAM_MEMBER_OPTIONS)}")
    print(f"Stations: {[s['name'] for s in STATION_OPTIONS]}")
    print(f"Properties to create: 11")
    print()

    database_id = create_database()

    if database_id:
        print("Next steps:")
        print("1. Open hhg-skill-audit.html")
        print("2. The database ID is already embedded (or update if different)")
        print("3. Start auditing!")
        log_exit("main", "Success")
        return 0
    else:
        print("Database creation failed. See errors above.")
        log_exit("main", "Failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
