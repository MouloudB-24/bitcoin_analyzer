from api_service import coindesk_api_get_echanges_rates


if __name__ == "__main__":
    rates = coindesk_api_get_echanges_rates()
    print(f"{'Date'}: {'Price close (€)'}")
    for rate in rates:
        print(f"{rate[0]}: {rate[1]}")