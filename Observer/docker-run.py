from project import app


if __name__ == "__main__":
    port = 5002
    print(f"Running Observer port:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
