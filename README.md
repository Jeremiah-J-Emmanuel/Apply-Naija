# Apply-Naija

**A Centralized Tertiary Institution Application System for Nigeria**

> A project by Coding Lab 17: David Achibiri, Keira Mutoni, Ridaa Isaro, Jeremiah Emmanuel, Dedine Muckabucyana, Maellene Mpingazima
---

## Project Overview

In Nigeria, the current university admission process requires students to rank institutions in an order of preference. You can only apply to four schools and therefore, each school has a ranking from the first choice to the fourth choice.. Due to high application volumes, most universities consider only students who select them as their first choice. This creates **selection bias** and leads to high rejection rates — even for top-performing students.

**Apply-Naija** is a **console-based prototype** for a centralized application system that eliminates selection bias and increases students’ chances of studying their **preferred majors**. It allows students to apply to **multiple institutions** without ranking them and enables admissions officers to quickly review and manage applications.

---

## Problem Statement

* **65%** of UTME candidates fail to secure admission into their desired major or institution.
* This is because students are **limited to four applications**: 2 universities, 1 polytechnic, 1 innovation enterprise institution.
Institutions mostly consider only **first-choice candidates**.
* Rejected candidates either **retake UTME** to get admission because it is valid for only one year,  which they often get lower grades than the previous years, or they settle for unwanted majors.

---

##  Solution: Apply-Naija

Apply-Naija addresses these issues by:

* Allowing **multiple applications** with no ranked preferences.
* Ensuring admissions officers cannot identify which institution was selected first.
* Enabling universities to **update their capacity status** (open/closed) to manage intake proactively.
* Providing a centralized platform for **students and officers** to interact with the admission system efficiently.
* Enabling universities to review applications very speedily.

---

##  Features

| Module            | Description                                                                   |
| ----------------- | ----------------------------------------------------------------------------- |
| `Welcome.py`      | Displays the splash screen and launches the main user interface               |
| `student_func.py` | Handles student functions: applying to schools, viewing responses, etc.       |
| `student_env.py`  | Manages student-specific environments and interactions                        |
| `officer_env.py`  | Officer-side interface for reviewing and responding to applications           |
| `admin.py`        | Admin-level features (e.g., viewing system-wide stats, managing institutions) |
| `utilities.py`    | Terminal utilities for clearing screen, improving UX                          |

---

##  How to Use the Prototype
This prototype is a console based application, thus, it should be run on the command line or on the terminal.
### 1. Clone the Repository
git clone https://github.com/Jeremiah-J-Emmanuel/Apply-Naija_GroupCodingLab17-Education-PLP2
cd Apply-Naija_GroupCodingLab17-Education-PLP2


### 2. Run the Application
You should make use of the version of python that you have. The most common is python3, and that is what is used here.
python3 Welcome.py

### 3. User Flow

* **Student**: Register → Apply to multiple schools → View admission results.
* **Admissions Officer**: Log in → Review applicants → Accept/Reject applicants → Update school capacity.

---

##  More about Apply-Naija
You can take a look at out canva slide presentations that we presented in school for our summative.
 [View Slides & Diagrams](https://www.canva.com/design/DAGiiz-12Qk/yVfVX6yvPfh5WSKPdhtdcQ/edit)

## 🛠️ Tools

* **Python Programming language**
* **Structured Query Language, MySQL, and the aiven database server** for handling application data
* **Git and GitHub** for collaboration and version control
