from project import app


if __name__ == "__main__":
    port = 5001
    print(f"Running Simulator port:{port} \n")
    app.run(port=port, debug=True)
