from process_data import process_airwaybills


def main():
    try:
        airwaybills = process_airwaybills()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
