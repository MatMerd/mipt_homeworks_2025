try:
    print("Importing main module...")
    from python_2hw.main import app

    print("✓ Main module imported successfully")

    print("\nImporting uvicorn...")
    import uvicorn

    print("✓ Uvicorn imported successfully")

    print("\nStarting server on http://127.0.0.1:9000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    uvicorn.run(app, host="127.0.0.1", port=9000)

except Exception as e:
    print(f"\n Error: {e}")
    import traceback

    traceback.print_exc()
