from project import app


if __name__ == "__main__":
    port = 5000
    print(f"Running Configurator port:{port} \n")
    app.run(host="0.0.0.0", port=port, debug=True)
