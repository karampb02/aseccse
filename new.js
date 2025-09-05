<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GNDU Attendance Tracker</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
        }
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Custom scrollbar for better aesthetics */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
    </style>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="container mx-auto p-4 sm:p-6 lg:p-8 max-w-7xl">

        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-4xl font-bold text-gray-900">Attendance Tracker</h1>
            <p class="text-gray-600 mt-2">GNDU B.Tech (CSE) Semester-1 (2025-2026)</p>
        </header>

        <div id="password-gate" class="fade-in">
             <div class="max-w-md mx-auto bg-white rounded-xl shadow-md overflow-hidden md:max-w-2xl p-8 text-center">
                <h2 class="text-2xl font-semibold mb-4">Select Your Section</h2>
                <div class="flex justify-center gap-4">
                     <button onclick="promptForSection('A')" class="px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75 transition duration-300">Section A</button>
                     <button onclick="promptForSection('B')" class="px-6 py-3 bg-pink-600 text-white font-semibold rounded-lg shadow-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-opacity-75 transition duration-300">Section B</button>
                </div>
            </div>
        </div>

        <!-- Main Content - Hidden by default -->
        <main id="app" class="hidden fade-in">
            <!-- Controls -->
            <div class="bg-white p-4 rounded-xl shadow-md mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-4 w-full sm:w-auto">
                     <input id="subject" type="text" placeholder="Enter Subject Name" class="flex-grow sm:flex-grow-0 w-full sm:w-64 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                     <p id="date" class="text-sm font-medium text-gray-700 whitespace-nowrap"></p>
                </div>
                <div class="flex items-center gap-2 w-full sm:w-auto">
                    <button onclick="promptForPDFExport()" class="w-full sm:w-auto px-4 py-2 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 transition duration-300">Export PDF</button>
                    <button onclick="resetAttendance()" class="w-full sm:w-auto px-4 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600 transition duration-300">Reset</button>
                </div>
            </div>

            <!-- Attendance Table -->
            <div class="bg-white rounded-xl shadow-md overflow-hidden">
                 <div class="max-h-[60vh] overflow-y-auto">
                    <table class="w-full text-left">
                        <thead class="sticky top-0 bg-gray-50 z-10">
                            <tr>
                                <th class="p-4 font-semibold">Roll No.</th>
                                <th class="p-4 font-semibold">Student Name</th>
                            </tr>
                        </thead>
                        <tbody id="attendanceTable">
                            <!-- Rows will be injected by JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>
            
             <footer class="text-center mt-8 text-sm text-gray-500">
                <p>Created by Karamjit Singh & Avnoor Singh Bal</p>
            </footer>
        </main>
    </div>

<script>
    const studentsA = [
        "AARUSHI SETHI", "ABHAY SINGH", "ABHI VERMA", "AKARSHDEEP SINGH", "AKASHDEEP SINGH", "AMANAT SHARMA", "AMANDEEP KAUR", "AMRIK SINGH", "ANANYA SINGLA", "ANGEL GUPTA", "ANIKET", "ANKIT KUMAR", "ANMOLDEEP KAUR", "ANMOLPREET KAUR", "ANSH AHLAWAT", "ANUSHKA", "ARCHIE DHIR", "ARIHANT SHARMA", "ARMAAN DEORA", "ARMAANDEEP SINGH", "ARNAV CHANDEL", "ARSHDEEP SINGH (4654)", "ARSHDEEP SINGH (2374)", "ARYAN RAJ", "ARYANSH", "ASHIMA", "ATHARV KAUL", "AVNOOR SINGH BAL", "AVZ SHARMA", "AYUSH RAJ", "BALGOPAL RAI SINGH", "BARINDERPAL SINGH", "BISHAV HANS", "BHAKTI GUPTA", "BHAUMIK", "BHAVYA", "BHAVYA SHARMA", "BIRJOT KAUR", "CHAHAT", "CHAKSHIKA CHAWLA", "CHARU MALHOTRA", "CHAUDHARY ASHUTOSH KUMAR", "DEEPALI LUTHRA", "DEEPIKA", "DEVAM SAGGU", "DEVANG", "DHRUV PATHANIA", "DHRUV SHARMA", "DILJOT KAUR", "DIVYA", "DINKAR MITTAL", "DIPTI", "DIVJOT SINGH (4304)", "DIVJOT SINGH (1522)", "DIVYANSH", "GARIMA TRIKHA", "GARV SEHGAL", "GOUTAM KUMAR", "GURANGAD SINGH", "GURANSHPREET SINGH", "GURJASHAN SINGH", "GURMANNAT KAUR", "GURMEET SINGH", "GURNOOR KAUR", "GURNOOR SINGH (3550)", "GURNOOR SINGH (5591)", "GURPREET KAUR", "GURSAJ SINGH", "GURSEERAT KAUR", "GURSHAN SINGH (1755)", "GURSHAN SINGH (0584)", "GURSIMRAN SINGH", "HAETAL KATARIA", "HARANSH SINGH", "HARGUN DEEP SINGH", "HARJAP SINGH", "HARKIRAT SINGH RIAR", "HARMANJOT SINGH", "HARNEET KAUR", "HARNOOR KAUR", "HARSHIL GUPTA (2273)", "HARSHIL GUPTA (5023)", "HARSHIT MALHOTRA", "HARSHIT MOHAN SHARMA", "HARSHPREET KAUR", "HARSIDAK SINGH", "HARWINDER SINGH", "ISHAN SEHGAL", "ISHITA", "ISHMEET KAUR", "ISHMEET SINGH", "JAGJIT SINGH", "JAGWINDER SINGH", "JAHIRUL ISLAM JOY", "JAHNAVI", "JAHNVI UCHARIA", "JASDEEP KAUR", "JASHANPREET SINGH", "JASKARANJEET SINGH", "JASKIRAT KAUR", "JASLEEN KAUR", "JASMIN KAUR SANDHU", "JASMINE KAUR", "JASPREET KAUR", "JATIN BERI", "JITISH MONGA", "KARAMJIT SINGH", "KARAN SINGH", "KARSIMRAN SINGH", "KASHIKA", "KAVYA ARORA", "KESHAV PURI", "KHUSHAAN LAL", "KHUSHI MEHTA", "KHUSHPREET SINGH", "KIRT PAUL", "KOMALPREET KAUR", "KRISH BHAGAT", "KRISH GUMBER", "KRISH KUMAR", "KRISH NAYYAR", "KRISHAN CHOPRA", "KRISHI SONDHI", "KRISHNA", "KRITAGAYA BHATIA", "KRITIKA MEHTA", "KUNAL", "KUSHAGRAH JAIN"
    ];

    const studentsB = [
        "LAKSHDEEP SINGH", "MALHAR ARORA", "MANASVI", "MANJOT KAUR", "MANJOT SINGH", "MANPAWAN KAUR", "MANPREET KUMAR", "MANRAJDEEP SINGH", "MANTHAN ATTRI", "MANTHAN SHARMA", "MEHAK GUPTA", "MEHAK PADWAL", "MEHAKDEEP KAUR", "MEHAKPREET SINGH", "MEHAR JOLLY", "MISHTHI", "MITHILESHWAR", "MOHIT", "MOHIT SALWAN", "MOHIT SINGH", "MOULIK YADAV", "MR SAKSHAM", "MRIDULA", "MUSKAN", "NANDANI GARG", "NANDINI RATHORE", "NAVDEEP KAUR", "NAVJIT KAPIL", "NAVJOT KAUR", "NAVNEET KAUR", "NAVREET KAUR", "NAVYA", "NEELESH KALIA", "NIMISH SURI", "NIRJALA", "NITISH", "PALAK SHARMA", "PAVITERPREET SINGH", "PAVNEET SINGH", "PRABHNOOR KAUR", "PRABHNOOR SINGH", "PRANAV JOSHI", "PRINCE KUMAR", "PRITIKA", "PRIYANSH", "RAGHAV SHARMA", "RAGHUNANDAN", "RAHUL SHARMA", "RANVIR SINGH", "RASHMITA", "RAVDEEP KAUR", "RAYAN CHANDEL", "REHAN SINGH", "RIDHAMPREET SINGH", "RISHITA", "RIVANSHU BEHAL", "ROHINI SHARMA", "ROHIT KUMAR", "ROOPANSHI SHARMA", "RUDRAKSH MEHRA", "RUDRAKSH SHARMA", "RUHI", "SACHIN KUMAR", "SAHEJVEER SINGH", "SAHIBPREET SINGH", "SAHIL GUPTA", "SAKSHAM GUPTA", "SAMAIRA", "SAMRIDHI SHARMA", "SANCHI SHARMA", "SANYAM GAUTAM", "SATYAK GUPTA", "SAWAL PUSHKARNA", "SAWNI", "SHAGUN KAUR", "SHASHANK SHEKHAR", "SHATRUNJAY SINGH", "SHAURYA THAKUR", "SHIVANG GUPTA", "SHIVANSH SHUKLA", "SHIVJOT SINGH", "SHREYANSH", "SIDARTH ATTRI", "SIRTAJ SINGH", "SIYA", "SOURAV", "SUKHMANI", "SUKHMANJEET SINGH", "SUKHMANPREET", "SUKHPAL SINGH", "SUNAKSHI MEHTA", "SUNDRAM KUMAR", "SUNIDHI SOOD", "SURYA DEY", "SUSHANK BALHOTRA", "SUSHEN GUPTA", "TANDRIKA RANI KUNDU", "TANMYA MAHAJAN", "TEJ AL CHOPRA", "TRIBHUVAN SINGH", "TUSHAAR", "UJWAL", "UTTAMPREET KAUR", "VAIBHAV MAHAJAN", "VAISHALI KUNDAL", "VARENYA MAHAJAN", "VARUN ALOONA", "VENU GOPAL", "VINEET KUMAR", "VINOD PARMAR", "VISHAL CHOUDHARY", "VISHESH KUMAR", "YASHIKA", "YOGITA", "YUVRAJ JASSI", "JATIN"
    ];

    let currentStudents = [];
    
    const dateObj = new Date();
    const d = dateObj.getDate();
    const m = dateObj.getMonth() + 1;
    const y = dateObj.getFullYear();
    document.getElementById("date").innerHTML = `<b>Date:</b> ${d}/${m}/${y}`;

    function promptForSection(section) {
        const password = prompt(`Enter password for Section ${section}:`);
        const correctPassword = section === 'A' ? '@Asec' : '@Bsec';
        if (password === correctPassword) {
            document.getElementById('password-gate').classList.add('hidden');
            document.getElementById('app').classList.remove('hidden');
            loadSection(section);
        } else if (password !== null) {
            alert('Incorrect password. Please try again.');
        }
    }
    
    function loadSection(section) {
        currentStudents = section === 'A' ? studentsA : studentsB;
        renderTable();
    }

    function renderTable() {
        const tableBody = document.getElementById('attendanceTable');
        tableBody.innerHTML = ''; // Clear existing rows
        currentStudents.forEach((name, index) => {
            const row = tableBody.insertRow();
            row.className = 'border-t border-gray-200 hover:bg-gray-50 cursor-pointer';
            row.insertCell(0).textContent = index + 1;
            row.cells[0].className = 'p-4 text-gray-700';
            row.insertCell(1).textContent = name;
            row.cells[1].className = 'p-4 text-gray-900 font-medium';
            row.classList.add('absent');

            row.addEventListener('click', () => {
                row.classList.toggle('present');
                row.classList.toggle('absent');
                if (row.classList.contains('present')) {
                    row.style.backgroundColor = '#d1fae5'; // A nice green
                } else {
                    row.style.backgroundColor = '';
                }
            });
        });
    }

    function getPresent() {
        return Array.from(document.querySelectorAll("#attendanceTable tr.present"))
            .map(row => `${row.cells[0].textContent}. ${row.cells[1].textContent}`);
    }

    function getAbsent() {
        return Array.from(document.querySelectorAll("#attendanceTable tr.absent"))
            .map(row => `${row.cells[0].textContent}. ${row.cells[1].textContent}`);
    }
    
    function promptForPDFExport() {
        const password = prompt("Please enter the password to export as PDF:");
        if (password === "@exportPDF") {
            exportPDF();
        } else if (password !== null) {
            alert("Incorrect password.");
        }
    }

    function exportPDF() {
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();
        const present = getPresent();
        const absent = getAbsent();
        const pageHeight = doc.internal.pageSize.getHeight();
        let yPos = 30;
        const lineHeight = 7;
        const subjectName = document.getElementById("subject").value || "N/A";

        doc.setFontSize(18);
        doc.text(`Attendance Report`, 14, 15);
        doc.setFontSize(11);
        doc.setTextColor(100);
        doc.text(`Subject: ${subjectName}`, 14, 22);
        doc.text(`Date: ${d}/${m}/${y}`, 14, 28);
        doc.text(`Present: ${present.length}, Absent: ${absent.length}, Total: ${currentStudents.length}`, 14, 34);

        yPos = 45;
        doc.setFontSize(12);
        doc.setTextColor(40, 167, 69);
        doc.text("Present Students:", 14, yPos);
        yPos += lineHeight + 2;
        doc.setFontSize(10);
        doc.setTextColor(0);
        present.forEach(line => {
            if (yPos > pageHeight - 20) { doc.addPage(); yPos = 20; }
            doc.text(line, 14, yPos);
            yPos += lineHeight;
        });

        yPos += lineHeight;
        doc.setFontSize(12);
        doc.setTextColor(220, 53, 69);
        doc.text("Absent Students:", 14, yPos);
        yPos += lineHeight + 2;
        doc.setFontSize(10);
        doc.setTextColor(0);
        absent.forEach(line => {
            if (yPos > pageHeight - 20) { doc.addPage(); yPos = 20; }
            doc.text(line, 14, yPos);
            yPos += lineHeight;
        });
        
        doc.save(`attendance-${subjectName.replace(' ','-')}-${d}-${m}-${y}.pdf`);
    }

    function resetAttendance() {
        if (confirm("Are you sure you want to reset all attendance marks?")) {
            renderTable();
        }
    }

</script>

</body>
</html>

