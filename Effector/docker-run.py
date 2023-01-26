from project import app


if __name__ == "__main__":
    port = 5003
    print(f"Running Effector port:{port} \n")
    app.run(host="0.0.0.0", port=port, debug=True)
