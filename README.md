<p>Python script that generates a random N length string given some parameters. Useful for generating passwords, keys or GUIDs</p>

<h1>Required Dependencies</h1>
    <ul>
        <li>Python</li>
        <ul>
            <li>Version >= 3.6</li>
            <li>Installation: <a href="https://www.python.org/downloads/">Link</a></li>
        </ul> 
        <li>Python Modules</li>
        <ul>
            <li>Cryptodomex</li> 
                <li>Purpose: 256-Bit AES</li>
                <li>Installation: <a href="https://pypi.org/project/pycryptodomex/">Link</a></li>
        </ul>
    </ul> 
    
<h1>Functionality</h1>
    <ul>
        <li>Generates N number of N character strings</li>
        <li>Command Line Parameters</li>
            <ul>
                <li>[Required] char - password character length</li>
                <li>[Required] num - number of strings to generate
                <li>[Optional] filter - these characters that will be excluded from the generated string</li>
                <li>[Optional] lc - include at least one lowercase alphabet character (Default is digits only)</li>
                <li>[Optional] uc - include at least one uppercase alphabet character (Default is digits only)</li>
                <li>[Optional] punc - include at least one puncuation character (Default is digits only)</li>
                <li>[Optional] unique - each character of the string will be unique (No duplicates)</li>
                <li>[Optional] conf - include a confirmation prompt</li>
                <li>[Optional] txt - outputs the generated password to a .txt file</li>
                <li>[Optional] etxt - outputs the generated password to an encrypted .txt file </li>
        </ul>
    </ul>
