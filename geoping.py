import json
import subprocess
import matplotlib.pyplot as plt

def load_servers(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def ping_host(hostname):
    """Ping a hostname and return the average round-trip time."""
    try:
        # Run the ping command
        result = subprocess.run(
            ['ping', '-c', '4', hostname],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output = result.stdout
        for line in output.splitlines():
            if "avg" in line:
                # Extract the average time
                avg_time = line.split('/')[4]
                return float(avg_time)
    except Exception as e:
        print(f"Error pinging {hostname}: {e}")
        return None

def extract_hostname(url):
    """Extract the hostname from a URL."""
    url = url.split("//")[-1]
    url = url.rstrip("/")
    return url

def main():
    data = load_servers('servers.json')
    results = {}

    for group in data:
        label = group["label"]
        for option in group["options"]:
            name = option["name"]
            url = option["url"]
            hostname = extract_hostname(url)

            print(f"Pinging {name} ({hostname})...")
            avg_time = ping_host(hostname)

            if avg_time is not None:
                results[name] = avg_time
                print(f"Average ping time for {name}: {avg_time} ms")
            else:
                print(f"Failed to ping {name}.")


    if results:
        plt.figure(figsize=(10, 5))
        plt.bar(results.keys(), results.values(), color='skyblue')
        plt.xlabel('Location')
        plt.ylabel('Average Ping Time (ms)')
        plt.title('Average Ping Time to Server Locations')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('ping_results.png')
        print("Plot saved as 'ping_results.png'")
        plt.show()

if __name__ == "__main__":
    main()