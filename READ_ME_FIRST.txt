PROJECT: System Health Monitoring Dashboard (Windows)

---

## FEATURES:

* Real-time CPU and RAM monitoring
* Dark mode graphical interface (GUI)
* Progress bars for usage visualization
* Status indicator (Normal / Medium / High)
* Start and Stop monitoring controls
* Top processes listing (sorted by memory usage)
* Automatic data logging (CSV, text log, HTML report)

---

## REQUIREMENTS:

* Python 3.x installed
* No external libraries required

---

## STEP 1: OPEN PROJECT FOLDER IN CMD

1. Place the project folder anywhere (e.g., Desktop)

2. Open Command Prompt

3. Navigate using "cd" command:

Example:
cd Desktop
cd "Capstone project"

(Use quotes if folder name has spaces)

4. Check files:
   dir

You should see:
monitor_gui_final.py

---

## STEP 2: RUN THE PROJECT

In the same Command Prompt:

python monitor_gui_final.py

OR (if python doesn't work):
py monitor_gui_final.py

---

## STEP 3: USING THE APPLICATION

* Click "Start" to begin monitoring
* CPU and RAM usage update in real time
* Progress bars visually show usage
* Status changes based on CPU load:

  * Normal (Green)
  * Medium Load (Yellow)
  * High Load (Red)
* Top processes are displayed (sorted by memory usage)
* Click "Stop" to stop monitoring

---

## OUTPUT FILES GENERATED:

* system_data.csv  → stores time, CPU, RAM
* system_log.txt   → detailed logs
* report.html      → open in browser

---

## STEP 4: VIEW REPORT

Double-click "report.html"
(It opens in your browser)

---

## TROUBLESHOOTING:

1. If 'python' is not recognized:
   Use: py monitor_gui_final.py

2. If permission issues occur:
   Run Command Prompt as Administrator

3. If no processes appear:
   Wait a few seconds after clicking Start

---

## NOTE:

* Do not rename the Python file
* Keep all files in the same folder
* Internet is not required to run the project

---

## END OF INSTRUCTIONS
