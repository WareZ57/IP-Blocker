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
<img width="502" height="432" alt="image" src="https://github.com/user-attachments/assets/c6c321b9-bd10-45cc-b102-8e5b21d966eb" />

You must run the script/EXE as an administrator.

The .exe may be detected as a false positive.
If you don’t want to use the compiled EXE version, use the non-compiled script instead.

https://www.virustotal.com/gui/file/7122d2f2b60d83ae5581da902bc9745d38ccf3fa02e2598c1231635d24a16d29?nocache=1

MD5 : c392d6e9b0066458c7927dd1444f34e6
