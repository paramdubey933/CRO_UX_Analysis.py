import random
pages = ["home", "product", "cart", "payment"]
def simulate_user_journey():
    journey = []
    for page in pages:
        if random.random() < 0.8:  
            journey.append(page)
        else:
            break
    return journey

user_data = {}
for i in range(1, 101):
    user_id = f"user{i}"
    user_data[user_id] = simulate_user_journey()

funnel_counts = {page: 0 for page in pages}
for journey in user_data.values():
    for page in journey:
        funnel_counts[page] += 1

print("Funnel counts:", funnel_counts)
conversion_rates = {}
total_users = len(user_data)

for i, page in enumerate(pages):
    if i == 0:
        conversion_rates[page] = funnel_counts[page] / total_users * 100
    else:
        prev_page = pages[i-1]
        if funnel_counts[prev_page] > 0:
            conversion_rates[page] = funnel_counts[page] / funnel_counts[prev_page] * 100
        else:
            conversion_rates[page] = 0

print("\nConversion Rates (step by step):")
for page, rate in conversion_rates.items():
    print(f"{page}: {rate:.2f}%")

final_conversion = funnel_counts["payment"] / total_users * 100
print(f"\nFinal Conversion Rate (home → payment): {final_conversion:.2f}%")
#simulates 100 users and runs through funnel with 80% prob. of success and then calculates things accordingly 
