# P2P-simulation

# P2P-simulation

Blockchain Assignment - By Sri Sanjay E (22N253)
Basic blockchain thing I made using Python (Flask) for the backend and a single HTML file (dashboard.html) as the frontend and app.py for backend

Features:

->You can create transactions (sender, receiver, amount)

->Mine a block (proof of work style with 0000 prefix)

->Register other nodes (just paste the URL and click register peer)

->Sync with longest chain (there’s a consensus button)

->See recent blocks and all mined transactions

Files Used:

app.py – Flask backend. Run this on different ports.

dashboard.html – UI.

How to Run:

# Make sure Python is installed.
            pip install flask requests
# Open one terminal:
            python app.py 5000
# Open another terminal:
            python app.py 5001
# Now open your browser and go to:
            http://localhost:5000

            http://localhost:5001

In port 5000 UI, paste:
            http://localhost:5001

into the peer input box and click “Register Peer”.

Then add transactions, mine a block, click sync chain on other port, see it update.

What You Can Do:

Create transaction — you fill in sender, receiver, amount.

Mine block — adds it to the chain and shows in recent blocks.

Register peer — tells the other node to sync with this.

Sync chain — pulls the longer chain from peers.

View mined transactions — lists all transactions that made it into blocks.

