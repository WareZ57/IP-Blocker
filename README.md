# IP-Blocker
Block IPs range in windows Firewall

**Features of the IP BLOCKER Script :**

- Allows entering multiple IP prefixes (format X.Y, e.g., 199.199) in a multiline text input.
- Automatically validates each IP prefix to ensure it follows the expected format (two numbers between 1 and 255 separated by a dot).
- Manages a single firewall rule in Windows:
- If the rule already exists, the script adds only the new IP ranges without creating duplicates.
- Otherwise, it creates the rule with the entered IP ranges.
- IP ranges are blocked in “full range” mode, meaning from X.Y.1.1 to X.Y.255.255.
- In case of issues (invalid IP, empty rule name, system error), the script displays clear error messages.
- The script deletes and recreates the rule on each update to ensure consistency of the blocked IPs.
