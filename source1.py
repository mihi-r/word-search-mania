# Word Search Mania under the MIT License
#
# Copyright (c) 2018 Mihir Patel
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import sys
import random
import string
import PyQt5.QtCore
from PyQt5.QtGui import QPixmap, QFont, QColor, QBrush, QTextCursor
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QPushButton, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QCheckBox, QMessageBox, \
    QTextEdit, QTableWidget, QProgressBar, QAbstractScrollArea, \
    QAbstractItemView, QLCDNumber, QTableWidgetItem, QApplication


nElements = 20
wordBoxChecked = False
rowBoxChecked = False
columnBoxChecked = False
diagonalBoxChecked = False


class StartMenu(QWidget):
    """Display window to configure the word search.

    Display options to:
        1. Select the number of rows for the word search grid
        2. Customize the game further
        3. Start the game
        4. Quit the game
    """

    def __init__(self):
        """Initiate initUI."""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initiate UI elements."""
        self.setWindowTitle("Word Search Mania")

        self.slider = QSlider(PyQt5.QtCore.Qt.Horizontal)
        self.sliderLabel = QLabel()
        self.configSlider()
        self.slider.valueChanged.connect(self.nRowDisplayChanged)

        self.difficultyLevel = QLabel()
        self.nRowDisplay = QLabel()
        self.configElementDisplay()

        buttonStart = QPushButton('Start')
        buttonStart.clicked.connect(self.onClickStart)

        buttonQuit = QPushButton('Quit')
        buttonQuit.clicked.connect(self.onClickQuit)

        buttonCustomize = QPushButton('Customize')
        buttonCustomize.clicked.connect(self.onClickCustomize)

        logoImage = QLabel()
        logoImage.setGeometry(10, 10, 10, 10)
        logoImage.setPixmap(QPixmap("logo.png").scaledToWidth(500))

        hBox = QHBoxLayout()
        hBox.addWidget(buttonQuit)
        hBox.addWidget(buttonCustomize)
        hBox.addWidget(buttonStart)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(logoImage, 0, 0)
        grid.addWidget(self.sliderLabel, 1, 0)
        grid.addWidget(self.difficultyLevel, 2, 0)
        grid.addWidget(self.slider, 3, 0)
        grid.addWidget(self.nRowDisplay, 4, 0)
        grid.addLayout(hBox, 5, 0)

        self.show()

    def configSlider(self):
        """Configure slider attributes and slider label."""
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setRange(10, 40)
        self.slider.setTickInterval(5)
        self.slider.setSingleStep(5)
        self.slider.setValue(nElements)

        self.sliderLabel.setText("How many rows would you like?")
        self.sliderLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.sliderLabel.setFont(QFont("Futura", 20))

    def configElementDisplay(self):
        """Configure difficulty label and display n row number."""
        self.difficultyLevel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.difficultyLevel.setText("Medium")
        self.difficultyLevel.setStyleSheet("color: rgb(255, 193, 37)")

        self.nRowDisplay.setText(str(self.slider.value()))
        self.nRowDisplay.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.nRowDisplay.setFont(QFont("Futura", 30))
        self.nRowDisplay.setStyleSheet("color: rgb(0, 170, 240)")

    def getSliderValue(self):
        """Get value from slider."""
        global nElements
        nElements = self.slider.value()

    def nRowDisplayChanged(self):
        """Change n row number to slider value and change difficulty label."""
        self.nRowDisplay.setText(str(self.slider.value()))
        if 10 <= self.slider.value() < 20:
            self.difficultyLevel.setText("Easy")
            self.difficultyLevel.setStyleSheet("color: rgb(67, 205, 128)")
        elif 20 <= self.slider.value() < 30:
            self.difficultyLevel.setText("Medium")
            self.difficultyLevel.setStyleSheet("color: rgb(255, 193, 37)")
        else:
            self.difficultyLevel.setText("Hard")
            self.difficultyLevel.setStyleSheet("color: rgb(255, 99, 71)")

    def onClickStart(self):
        """Open main app on button click start."""
        self.getSliderValue()
        self.close()
        self.openApp = App()
        self.openApp.show()

    def onClickQuit(self):
        """Exit window on button click button quit."""
        sys.exit()

    def onClickCustomize(self):
        """Initiate customize menu on button click customize."""
        self.close()
        self.openCustomizeMenu = CustomizeMenu()
        self.openCustomizeMenu.show()


class CustomizeMenu(QWidget):
    """Display window to customize the word search.

    Display options to:
        1. Add custom words
        2. Configure how words are generated
        3. Continue if done customizing

    Raise pop-ups if configuration limits are not met.
    """

    def __init__(self):
        """Initiate initUI."""
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initiate UI elements."""
        self.setWindowTitle("Customize")

        self.cBoxWords = QCheckBox('Check to add custom words', self)
        self.cBoxWords.stateChanged.connect(self.wordBoxChecked)
        self.cBoxWords.setToolTip('Check to add custom words')

        self.cBoxRows = QCheckBox('Rows')
        self.cBoxRows.stateChanged.connect(self.rowBoxChecked)
        self.cBoxRows.setToolTip('Check the "row" box to generate words horizontally')

        self.cBoxColumns = QCheckBox('Columns')
        self.cBoxColumns.stateChanged.connect(self.columnBoxChecked)
        self.cBoxColumns.setToolTip('Check the "columns" box to generate words vertically')

        self.cBoxDiagonals = QCheckBox('Diagonals')
        self.cBoxDiagonals.stateChanged.connect(self.diagonalBoxChecked)
        self.cBoxDiagonals.setToolTip('Check the "diagonals" box to generate words diagonally')

        buttonContinue = QPushButton('Continue', self)
        buttonContinue.clicked.connect(self.onClickContinue)

        # Head title
        title = QLabel()
        title.setText('Customize')
        title.setFont(QFont("Futura", 50))
        title.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        # Horizontal box that contains the title
        titleBox = QHBoxLayout()
        titleBox.addWidget(title)

        # Description above right hand checkboxes
        cBoxDescription = QLabel()
        cBoxDescription.setText('How would you like\nthe words to be generated?')

        # Text box to add custom words
        self.addWordBox = QTextEdit()
        self.addWordBox.setMaximumWidth(200)
        self.addWordBox.setMaximumHeight(150)
        self.addWordBox.setToolTip('Words must be at least 3 characters long!')
        self.addWordBox.setReadOnly(True)

        vBox = QVBoxLayout()
        vBox.addWidget(cBoxDescription)
        vBox.addWidget(self.cBoxRows)
        vBox.addWidget(self.cBoxColumns)
        vBox.addWidget(self.cBoxDiagonals)
        vBox.addWidget(buttonContinue)

        vBox2 = QVBoxLayout()
        vBox2.addWidget(self.cBoxWords)
        vBox2.addWidget(self.addWordBox)

        grid = QGridLayout()
        grid.addLayout(vBox2, 1, 0)
        grid.addLayout(vBox, 1, 1)

        vBoxOuter = QVBoxLayout()
        self.setLayout(vBoxOuter)
        vBoxOuter.addWidget(title)
        vBoxOuter.addLayout(grid)

        self.show()

    def wordBoxChecked(self):
        """Allow text to be entered into word box if checked."""
        global wordBoxChecked
        if self.cBoxWords.isChecked():
            self.addWordBox.setReadOnly(False)
            wordBoxChecked = True
        else:
            self.addWordBox.setReadOnly(True)
            wordBoxChecked = False

    def rowBoxChecked(self):
        """Set row generation to true if checked."""
        global rowBoxChecked
        if self.cBoxRows.isChecked():
            rowBoxChecked = True
        else:
            rowBoxChecked = False

    def columnBoxChecked(self):
        """Set column generation to true if checked."""
        global columnBoxChecked
        if self.cBoxWords.isChecked():
            columnBoxChecked = True
        else:
            columnBoxChecked = False

    def diagonalBoxChecked(self):
        """Set diagonal generation to true if checked."""
        global diagonalBoxChecked
        if self.cBoxWords.isChecked():
            diagonalBoxChecked = True
        else:
            diagonalBoxChecked = False

    def onClickContinue(self):
        """Open main app window if limits met; raise pop-ups otherwise."""
        if not self.cBoxRows.isChecked() and not self.cBoxColumns.isChecked() and not self.cBoxDiagonals.isChecked():
            self.popUp()

        elif self.cBoxWords.isChecked():
            customWords = self.addWordBox.toPlainText()
            wordList = customWords.split()
            for x in wordList:
                if len(x) < 3:
                    self.popUp4()
                elif x.isalpha():
                    x = x.lower()
                    with open('custom_word_bank.txt', 'w') as customWordFile:
                        customWordFile.write(x + '\n')
                else:
                    self.popUp2()

            if len(wordList) < 5:
                self.popUp3()
            else:
                self.close()
                openApp = App()
                openApp.show()
        else:
            self.close()
            self.openApp = App()
            self.openApp.show()

    def popUp(self):
        """Raise pop-up when no generation direction is checked."""
        popup = QMessageBox()
        popup.warning("Error", 'Please select at least one direction to generate words', QMessageBox.Ok)
        if popup == QMessageBox.Ok:
            pass

    def popUp2(self):
        """Raise pop-up when non-alphanumeric characters are used."""
        popup2 = QMessageBox()
        popup2.warning("Error", 'Only alphanumeric characters are aloud!', QMessageBox.Ok)
        if popup2 == QMessageBox.Ok:
            pass

    def popUp3(self):
        """Raise pop-up when less than 5 words are entered."""
        popup3 = QMessageBox()
        popup3.warning("Error", 'You must enter in at least 5 words!', QMessageBox.Ok)
        if popup3 == QMessageBox.Ok:
            pass

    def popUp4(self):
        """Raise pop-up when custom words contain less than 3 characters."""
        popup4 = QMessageBox()
        popup4.warning("Error", 'Custom words must be contain at least 3 characters!', QMessageBox.Ok)
        if popup4 == QMessageBox.Ok:
            pass


class App(QWidget):
    """Display window for the main game and start the timer.

    Display options to:
        1. Select letters on the table
        2. Pause/Resume the game
        3. Quit the game

    Attributes:
        wordBank: A string of the words to find in the word search.
        wordBankSplit: A list of strings of words to find in the word search.
        wordSelected: A string to hold the current word selected.
        xVisited: A list of integers to hold the current row values of the letters selected.
        yVisited: A list of integers to hold the current column values of the letters selected.
        inRow: An integer to determine if the letters selected are in consecutive fashion.
        progressValue: An integer to keep track of the words found.
        wordsCompleted: A list of strings of the words found.
        timeFlag: A time flag to keep track of the timer if the game has been paused or resumed.
    """

    def __init__(self):
        """Initiate initUI."""
        super().__init__()
        self.wordBank = ""
        self.wordBankSplit = []
        self.wordSelected = ""
        self.xVisited = []
        self.yVisited = []
        self.inRow = 0
        self.progressValue = 0
        self.wordsCompleted = []
        self.timeFlag = 2
        self.initUI()

    def initUI(self):
        """Initiate UI elements."""
        title = 'Word Search Mania'
        self.setWindowTitle(title)

        self.wordBankBox = QTextEdit()
        self.tableWidget = QTableWidget()
        self.progress = QProgressBar()
        self.timer = PyQt5.QtCore.QTimer()

        self.createTable()
        self.createWordBank()
        self.createProgressBar()
        self.createTimer()
        self.mouseTracking()

        wordBankTitle = QLabel()
        wordBankTitle.setText("       Word Bank")
        font = QFont()
        font.setBold(True)
        wordBankTitle.setFont(font)

        buttonClear = QPushButton('Clear', self)
        buttonClear.setToolTip('This clears your word selection.')
        buttonClear.clicked.connect(self.onClickClear)

        buttonQuit = QPushButton('Quit', self)
        buttonQuit.setToolTip('This will buttonQuit your game. You will loose all progress.')
        buttonQuit.clicked.connect(self.onClickQuit)

        self.buttonPause = QPushButton('Pause')
        self.buttonPause.setToolTip('This pauses the game.')
        self.buttonPause.clicked.connect(self.onClickPause)

        vBox = QVBoxLayout()
        vBox.addWidget(wordBankTitle)
        vBox.addWidget(self.wordBankBox)
        vBox.addWidget(buttonClear)
        vBox.addWidget(self.buttonPause)
        vBox.addWidget(buttonQuit)

        self.grid = QGridLayout()
        self.grid.addLayout(vBox, 0, 1)
        self.grid.addWidget(self.tableWidget, 0, 0)
        self.grid.addWidget(self.progress, 1, 0)
        self.grid.addWidget(self.LCD, 1, 1)

        self.setLayout(self.grid)

        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.show()

    def createTable(self):
        """Generate the word search table."""
        generateAll = False

        global wordBoxChecked
        global rowBoxChecked
        global columnBoxChecked
        global diagonalBoxChecked

        if wordBoxChecked:
            f = open('custom_word_bank.txt', "r")
            wordBoxChecked = False
        else:
            f = open('words_alpha.txt', "r")
            generateAll = True

        wordFileContent = f.readlines()
        wordFileContent = [x.strip() for x in wordFileContent]

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(nElements)
        self.tableWidget.setColumnCount(nElements)

        # Populate table with random letters
        for y in range(0, nElements):
            for x in range(0, nElements):
                self.tableWidget.setItem(x, y, QTableWidgetItem(random.choice(string.ascii_uppercase)))
                self.tableWidget.setColumnWidth(x, 20)
                self.tableWidget.setRowHeight(y, 20)

        # Implements words across rows
        def generateRow(self):
            col = 0
            row = 0
            lastColPosition = 0
            wordDuplicate = False
            while row < nElements:
                while col < nElements:
                    col = random.randint(lastColPosition, nElements)
                    word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    while len(word) < 3:
                        word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    for x in self.wordBank.split():
                        if x == word:
                            wordDuplicate = True
                    if not wordDuplicate:
                        if nElements - col > len(word):
                            lastColPosition = len(word) + col
                            self.wordBank += word + "\n"
                            for x in word:
                                self.tableWidget.setItem(row, col, QTableWidgetItem(x))
                                col += 1
                            col = nElements
                    wordDuplicate = False
                row += 3
                col = 0
                lastColPosition = 0

        # Implements words down each column
        def generateCol(self):
            col = 0
            row = 0
            lastRowPosition = 0
            decide = 0
            wordDuplicate = False
            while col < nElements:
                while row < nElements:
                    row = random.randint(lastRowPosition, nElements)
                    word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    while len(word) < 3:
                        word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    for x in self.wordBank.split():
                        if x == word:
                            wordDuplicate = True
                    if not wordDuplicate:
                        if nElements - row > len(word):
                            for k in range(row, row + len(word)):
                                if self.tableWidget.item(k, col).text().islower():
                                    decide += 1
                            if decide == 0:
                                lastRowPosition = len(word) + row
                                self.wordBank += word + "\n"
                                for y in word:
                                    self.tableWidget.setItem(row, col, QTableWidgetItem(y))
                                    row += 1
                            decide = 0
                    wordDuplicate = False
                col += 3
                row = 0
                lastRowPosition = 0

        # Implements words down each diagonal in forward
        def generateForwardDiag(self):
            col = 0
            row = 0
            wordCount = 0
            decide = 0
            wordDuplicate = False
            while row < nElements:
                while col < nElements:
                    word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    while len(word) < 3:
                        word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    for x in self.wordBank.split():
                        if x == word:
                            wordDuplicate = True
                    if not wordDuplicate:
                        tempRow = row
                        tempCol = col
                        while tempRow < nElements and tempCol < nElements and wordCount < len(word):
                            if self.tableWidget.item(tempRow, tempCol).text().islower():
                                decide += 1
                            tempRow += 1
                            tempCol += 1
                            wordCount += 1
                        tempRow = row
                        tempCol = col
                        if decide == 0 and (len(word) + tempCol) < nElements and (len(word) + tempRow) < nElements:
                            self.wordBank += word + "\n"
                            for y in word:
                                self.tableWidget.setItem(tempRow, tempCol, QTableWidgetItem(y))
                                tempCol += 1
                                tempRow += 1
                    decide = 0
                    wordCount = 0
                    col += 1
                    wordDuplicate = False
                row += 1
                col = 0

        # Implements words down each diagonal in backward
        def generateBackwardDiag(self):
            col = nElements - 1
            row = 0
            wordCount = 0
            decide = 0
            wordDuplicate = False
            while row < nElements:
                while col >= 0:
                    word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    while len(word) < 3:
                        word = wordFileContent[random.randint(0, len(wordFileContent) - 1)]
                    for x in self.wordBank.split():
                        if x == word:
                            wordDuplicate = True
                    if not wordDuplicate:
                        tempRow = row
                        tempCol = col
                        while tempRow < nElements and tempCol >= 0 and wordCount < len(word):
                            if self.tableWidget.item(tempRow, tempCol).text().islower():
                                decide += 1
                            tempRow += 1
                            tempCol -= 1
                            wordCount += 1
                        tempRow = row
                        tempCol = col
                        if decide == 0 and (tempCol - len(word)) > 0 and (len(word) + tempRow) < nElements:
                            self.wordBank += word + "\n"
                            for y in word:
                                self.tableWidget.setItem(tempRow, tempCol, QTableWidgetItem(y))
                                tempRow += 1
                                tempCol -= 1
                    decide = 0
                    wordCount = 0
                    col -= 1
                    wordDuplicate = False
                row += 1
                col = nElements - 1

        if generateAll:
            generateRow(self)
            generateCol(self)
            generateForwardDiag(self)
            generateBackwardDiag(self)
        else:
            if rowBoxChecked:
                generateRow(self)
                rowBoxChecked = False
            if columnBoxChecked:
                generateCol(self)
                columnBoxChecked = False
            if diagonalBoxChecked:
                generateForwardDiag(self)
                generateBackwardDiag(self)
                diagonalBoxChecked = False

        for y in range(0, nElements):
            for x in range(0, nElements):
                letter = self.tableWidget.item(x, y).text().lower()
                self.tableWidget.setItem(x, y, QTableWidgetItem(letter))
                self.tableWidget.item(x, y).setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)

        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setShowGrid(False)
        self.tableWidget.clicked.connect(self.onClickLetter)

    def createWordBank(self):
        """Generate a word bank of the words to be found."""
        self.wordBankSplit = self.wordBank.split()
        self.wordBankSplit.sort()
        for x in self.wordBankSplit:
            self.wordBankBox.append(x)
        self.wordBankBox.setReadOnly(True)
        self.wordBankBox.setMaximumWidth(120)
        font = QFont()
        font.setFamily('Arial')
        self.wordBankBox.setFont(font)
        self.wordBankBox.moveCursor(QTextCursor.Start)

    def strikeWord(self, word):
        """Strike word with a line if the word is found."""
        newWord = ""
        for x in word:
            newWord += x + '\u0336'
        self.wordBankSplit = [newWord if i == word else i for i in self.wordBankSplit]
        self.wordBankBox.setText("")
        for x in self.wordBankSplit:
            self.wordBankBox.append(x)
        self.wordBankBox.show()
        self.wordBankBox.moveCursor(QTextCursor.Start)

    def mouseTracking(self):
        """Track mouse movement of the table."""
        self.currentHover = [0, 0]
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.cellEntered.connect(self.cellHover)

    def cellHover(self, row, column):
        """Highlight letter if mouse is hovering over it."""
        item = self.tableWidget.item(row, column)
        oldItem = self.tableWidget.item(self.currentHover[0], self.currentHover[1])
        mouseTracker1 = True
        mouseTracker2 = True
        for x in range(len(self.xVisited)):
            if self.xVisited[x] == row and self.yVisited[x] == column:
                mouseTracker1 = False
            if self.currentHover[0] == self.xVisited[x] and self.currentHover[1] == self.yVisited[x]:
                mouseTracker2 = False
        if mouseTracker1:
            if self.currentHover != [row, column]:
                if item.text().islower():
                    item.setBackground(QBrush(QColor('yellow')))
                if oldItem.text().islower() and mouseTracker2:
                    oldItem.setBackground(QBrush(QColor('white')))
        elif mouseTracker2:
            oldItem.setBackground(QBrush(QColor('white')))
        self.currentHover = [row, column]

    def onClickLetter(self):
        """Highlight letters on selection and highlight word green if found on click."""
        self.wordSelected = ""
        wordBankSplitOriginal = self.wordBank.split()
        selectionTracker = True
        selectionCorrectness = 0
        word = ""
        listX = []
        listY = []

        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            if self.tableWidget.item(currentQTableWidgetItem.row(), currentQTableWidgetItem.column()).text().isupper():
                letter = self.tableWidget.item(currentQTableWidgetItem.row(),
                                               currentQTableWidgetItem.column()).text().lower()
                self.tableWidget.setItem(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
                                         QTableWidgetItem(letter))
                self.tableWidget.clearSelection()
            else:
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    for x in range(0, len(self.xVisited)):
                        if currentQTableWidgetItem.row() == self.xVisited[x] and currentQTableWidgetItem.column() == \
                                self.yVisited[x]:
                            selectionTracker = False
                    if selectionTracker:
                        letter = self.tableWidget.item(currentQTableWidgetItem.row(),
                                                       currentQTableWidgetItem.column()).text().upper()
                        self.tableWidget.setItem(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(),
                                                 QTableWidgetItem(letter))
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    if selectionTracker:
                        self.tableWidget.item(currentQTableWidgetItem.row(),
                                              currentQTableWidgetItem.column()).setBackground(QColor(216, 191, 216))
                for currentQTableWidgetItem in self.tableWidget.selectedItems():
                    if selectionTracker:
                        self.tableWidget.item(currentQTableWidgetItem.row(),
                                              currentQTableWidgetItem.column()).setTextAlignment(
                            PyQt5.QtCore.Qt.AlignCenter)
                    self.tableWidget.clearSelection()

        for x in range(0, nElements):
            for y in range(0, nElements):
                if self.tableWidget.item(x, y).text().isupper():
                    self.wordSelected += self.tableWidget.item(x, y).text()
                    listX.append(x)
                    listY.append(y)
        for x in wordBankSplitOriginal:
            if x == self.wordSelected.lower():
                selectionCorrectness += 1
                word = x
        if selectionCorrectness == 1:  # Makes sure the word is in a row
            for i in range(1, len(listY)):
                if listY[i - 1] == listY[i] - 1 and listX[i - 1] == listX[i]:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a single column
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i]:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a forward diagonal
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i] - 1:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0
        if selectionCorrectness == 1:  # Makes sure the word is in a backward diagonal
            for i in range(1, len(listY)):
                if listX[i - 1] == listX[i] - 1 and listY[i - 1] == listY[i] + 1:
                    self.inRow += 1
                if self.inRow == len(listY) - 1:
                    selectionCorrectness += 1
                    self.inRow = 0

        if selectionCorrectness == 2:
            wordIndex = self.wordSelected.find(word)
            self.progressValue += 1
            self.setProgressBar()
            self.strikeWord(word)
            self.wordsCompleted.append(word)
            for i in range(wordIndex, wordIndex + len(word)):
                letterI = self.tableWidget.item(listX[i], listY[i]).text().lower()
                self.tableWidget.setItem(listX[i], listY[i], QTableWidgetItem(letterI))
            for i in range(wordIndex, wordIndex + len(word)):
                self.tableWidget.item(listX[i], listY[i]).setBackground(QColor(144, 238, 144))
                self.xVisited.append(listX[i])
                self.yVisited.append(listY[i])
            for i in range(wordIndex, wordIndex + len(word)):
                self.tableWidget.item(listX[i], listY[i]).setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)

    def onClickClear(self):
        """Clear word selection on button click."""
        self.wordSelected = ""
        for x in range(0, nElements):
            for y in range(0, nElements):
                if self.tableWidget.item(x, y).text().isupper():
                    letterI = self.tableWidget.item(x, y).text().lower()
                    self.tableWidget.setItem(x, y, QTableWidgetItem(letterI))
                    self.tableWidget.item(x, y).setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)

    def onClickQuit(self):
        """Display option to quit the app on button click."""
        quitMessage = QMessageBox()
        quitMessage = QMessageBox.question(self, "Quit", "Are you sure you would like to buttonQuit?",
                                           QMessageBox.No | QMessageBox.Yes)
        if quitMessage == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def createProgressBar(self):
        """Generate progress bar of with the progress of the words found until completion."""
        self.progress.setRange(0, len(self.wordBank.split()))
        self.progress.setToolTip("Shows your word completion progress.")

    def setProgressBar(self):
        """Set value for the progress bar."""
        self.progress.setValue(self.progressValue)

    def createTimer(self):
        """Generate a timer."""
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)
        self.time = PyQt5.QtCore.QTime(0, 0, 0)

        self.LCD = QLCDNumber()
        self.LCD.display(self.time.toString("hh:mm:ss"))
        self.LCD.setSegmentStyle(QLCDNumber.Flat)

    def Time(self):
        """Increment timer by a second."""
        self.time = self.time.addSecs(1)
        self.LCD.display(self.time.toString("hh:mm:ss"))

        if len(self.wordsCompleted) == len(self.wordBankSplit):
            self.timer.stop()
            self.endTime = self.time.toString("hh:mm:ss")
            self.addHighScore()
            self.close()
            self.openHighscoreMenu = HighScoreMenu()
            self.openHighscoreMenu.show()

    def onClickPause(self):
        """Pause and resume the game on button click."""
        if self.timeFlag % 2 == 0:
            self.timer.stop()
            self.timeFlag += 1
            self.tableWidget.hide()
            self.buttonPause.setText("Unpause")
        else:
            self.timer.start()
            self.timeFlag += 1
            self.tableWidget.show()
            self.tableWidget.clearSelection()
            self.buttonPause.setText("Pause")

    def addHighScore(self):
        """Save highScore to WS_Highscores text file."""
        with open("highscores.txt", "a") as highscoreFile:
            if 10 <= nElements <= 19:
                highscoreFile.write("Easy\n")
            elif 20 <= nElements <= 29:
                highscoreFile.write("Medium\n")
            else:
                highscoreFile.write("Hard\n")
            highscoreFile.write(str(self.endTime) + "\n")


class HighScoreMenu(QWidget):
    """Display window to report current and previous high scores

    Display options to:
        1. Start new game
        2. Quit the game
    """
    def __init__(self):
        """Initiate initUI."""
        super().__init__()

        self.initUI()

    def initUI(self):
        """Initiate UI elements."""
        self.setWindowTitle("Word Search Mania")

        self.contents = ""

        with open("highscores.txt", "r") as highscoreFile:
            self.contents = highscoreFile.readlines()
            self.contents = [x.strip() for x in self.contents]

        self.easyBoard = QTextEdit()
        self.easyBoard.setReadOnly(True)
        self.easyBoard.setMaximumWidth(150)
        self.easyBoard.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.mediumBoard = QTextEdit()
        self.mediumBoard.setReadOnly(True)
        self.mediumBoard.setMaximumWidth(150)
        self.mediumBoard.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.hardBoard = QTextEdit()
        self.hardBoard.setReadOnly(True)
        self.hardBoard.setMaximumWidth(150)
        self.hardBoard.setAlignment(PyQt5.QtCore.Qt.AlignCenter)

        titleLabel = QLabel()
        titleLabel.setText("High Scores")
        titleLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        titleLabel.setFont(QFont("Futura", 30))
        easyLabel = QLabel()
        easyLabel.setText("Easy Mode")
        easyLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        easyLabel.setToolTip("The game is in easy mode if you chose rows 10 - 19.")
        mediumLabel = QLabel()
        mediumLabel.setText("Medium Mode")
        mediumLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        mediumLabel.setToolTip("The game is in medium mode if you chose rows 20 - 29.")
        hardLabel = QLabel()
        hardLabel.setText("Hard Mode")
        hardLabel.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        hardLabel.setToolTip("The game is in hard mode if you chose rows 30 - 40.")

        for x in range(0, len(self.contents), 2):
            if self.contents[x] == "Easy":
                self.addEasyBoard(self.contents[x + 1])
            if self.contents[x] == "Medium":
                self.addMediumBoard(self.contents[x + 1])
            if self.contents[x] == "Hard":
                self.addHardBoard(self.contents[x + 1])

        self.buttonStartOver = QPushButton()
        self.buttonStartOver.setText("Play Again")
        self.buttonStartOver.clicked.connect(self.onClickStartOver)

        self.buttonQuit = QPushButton()
        self.buttonQuit.setText("Quit")
        self.buttonQuit.clicked.connect(self.onClickQuit)


        self.createHighScoreDisplay()

        HBoxLabel = QHBoxLayout()
        HBoxLabel.addWidget(easyLabel)
        HBoxLabel.addWidget(mediumLabel)
        HBoxLabel.addWidget(hardLabel)
        HBox = QHBoxLayout()
        HBox.addWidget(self.easyBoard)
        HBox.addWidget(self.mediumBoard)
        HBox.addWidget(self.hardBoard)
        HBoxButton = QHBoxLayout()
        HBoxButton.addWidget(self.buttonQuit)
        HBoxButton.addWidget(self.buttonStartOver)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(titleLabel, 0, 0)
        self.grid.addLayout(HBoxLabel, 1, 0)
        self.grid.addLayout(HBox, 2, 0)
        self.grid.addWidget(self.currentScore, 3, 0)
        self.grid.addWidget(self.highScore, 4, 0)
        self.grid.addLayout(HBoxButton, 5, 0)

        self.show()

    def addEasyBoard(self, score):
        """Populate scores score to easy section of the board."""
        self.easyBoard.append(score)

    def addMediumBoard(self, score):
        """Populate scores score to medium section of the board."""
        self.mediumBoard.append(score)

    def addHardBoard(self, score):
        """Populate scores to hard section of the board."""
        self.hardBoard.append(score)

    def onClickStartOver(self):
        """Open main app on button click start over."""
        self.close()
        self.openStartMenu = StartMenu()
        self.openStartMenu.show()

    def onClickQuit(self):
        """Display option to quit the app on button click."""
        self.quitMessage = QMessageBox()
        self.quitMessage = QMessageBox.question(self, "Quit", "Are you sure you would like to buttonQuit?",
                                                QMessageBox.No | QMessageBox.Yes)
        if self.quitMessage == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def createHighScoreDisplay(self):
        self.currentScore = QLabel()
        self.currentScore.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.currentScore.setFont(QFont("Futura", 14))

        self.highScore = QLabel()
        self.highScore.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.highScore.setFont(QFont("Futura", 14))

        highestScore = self.contents[len(self.contents) - 1]

        if int(highestScore[1]) > 0 or int(highestScore[0]) > 0:
            time = " hours"
        elif int(highestScore[4]) > 0 or int(highestScore[3]) > 0:
            time = " minutes"
        else:
            time = " seconds"

        self.currentScore.setText("You beat the word search in " + self.contents[len(self.contents) - 1]
                                  + time + " in " + self.contents[len(self.contents) - 2] + " Mode.")

        mode = self.contents[len(self.contents) - 2]

        for x in range(1, len(self.contents), 2):
            if highestScore > self.contents[x] and self.contents[x - 1] == mode:
                highestScore = self.contents[x]
        if highestScore == self.contents[len(self.contents) - 1]:
            self.highScore.setText("You beat your high score!")
        else:
            self.highScore.setText("You did not beat your high score of " + highestScore + " .")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = StartMenu()
    main.show()
    sys.exit(app.exec_())
