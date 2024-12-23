import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const CalculatorApp());
}

class CalculatorApp extends StatelessWidget {
  const CalculatorApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Calculator',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const CalculatorScreen(),
    );
  }
}

class CalculatorScreen extends StatefulWidget {
  const CalculatorScreen({Key? key}) : super(key: key);

  _CalculatorScreenState createState() => _CalculatorScreenState();
}

class _CalculatorScreenState extends State<CalculatorScreen> {
  final TextEditingController _functionController = TextEditingController();
  String _function = '';
  String _functionResult = '';
  String _graphBase64 = ''; // Store base64 encoded image data
  int _cursorPosition = 0;
  bool _showInverseKeys = false;

  @override
  void dispose() {
    _functionController.dispose();
    super.dispose();
  }

  void _onInputChanged(String value) {
    setState(() {
      _function = value;
      _functionController.text = value; // Update the controller
    });
  }

  void _onButtonPressed(String text) {
  setState(() {
    final int functionLength = _function.length;

    if (text == 'C') {
      _function = '';
      _functionResult = ''; // Clear the result
    } else if (text == '=') {
      if (_function.toLowerCase() == 'heroes') {
        // Display the pop-up dialog with the creators' names
        _showCreatorsDialog();
        return; // Exit the method to prevent further processing
      }
      // Prompt user to enter lower and upper bounds
      _showBoundsDialog();
    } else if (text == '⌫') {
      if (_function.isNotEmpty && _cursorPosition > 0) {
        _function = _function.substring(0, _cursorPosition - 1) +
            _function.substring(_cursorPosition);
        _cursorPosition--;
      }
    } else if (text == 'inv') {
      _showInverseKeys = !_showInverseKeys;
    } else if (_showInverseKeys) {
      _function += '$text('; // Add an open bracket after inverse trigonometric functions
      _showInverseKeys = false;
    } else if (['sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'asin', 'acos', 'atan', 'acsc', 'asec', 'acot', 'ln'].contains(text)) {
      _function += '$text(';
    } else {
      // If cursor is not used, insert text at the end of the function
      if (_cursorPosition == functionLength) {
        _function += text;
      } else {
        // Otherwise, insert text at the cursor position
        _function = _function.substring(0, _cursorPosition) +
            text +
            _function.substring(_cursorPosition);
        _cursorPosition++;
      }
    }

    // Update cursor position to be at the end of the function
    _cursorPosition = _function.length;

    _functionController.value = TextEditingValue(
      text: _function,
      selection: TextSelection.collapsed(offset: _cursorPosition),
    );
  });
}

// Function to show a dialog with creators' names
// Function to show a dialog with creators' names
// Function to show a dialog with creators' names
void _showCreatorsDialog() {
  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        backgroundColor: Colors.black, // Background color
        title: Text(
          'Creators:',
          style: TextStyle(
            color: Colors.green, // Text color
            fontSize: 24.0, // Font size
            fontFamily: 'RobotoMono', // Monospaced font
          ),
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              'The creators are:',
              style: TextStyle(
                color: Colors.green,
                fontSize: 18.0,
                fontFamily: 'RobotoMono',
              ),
            ),
            SizedBox(height: 16),
            Text(
              'Divyansh Khatikar',
              style: TextStyle(
                color: Colors.green,
                fontSize: 16.0,
                fontFamily: 'RobotoMono',
              ),
            ),
            Text(
              'Sharv Mahajan',
              style: TextStyle(
                color: Colors.green,
                fontSize: 16.0,
                fontFamily: 'RobotoMono',
              ),
            ),
            Text(
              'Pranav Mali',
              style: TextStyle(
                color: Colors.green,
                fontSize: 16.0,
                fontFamily: 'RobotoMono',
              ),
            ),
            Text(
              'Parth Patil',
              style: TextStyle(
                color: Colors.green,
                fontSize: 16.0,
                fontFamily: 'RobotoMono',
              ),
            ),
            Text(
              'Yash Mawale',
              style: TextStyle(
                color: Colors.green,
                fontSize: 16.0,
                fontFamily: 'RobotoMono',
              ),
            ),
          ],
        ),
        actions: <Widget>[
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
            },
            child: Text(
              'OK',
              style: TextStyle(
                color: Colors.green,
                fontSize: 18.0,
                fontFamily: 'RobotoMono',
              ),
            ),
          ),
        ],
      );
    },
  );
}




  Widget _buildButton(String text) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: ElevatedButton(
          onPressed: () => _onButtonPressed(text),
          style: ButtonStyle(
            backgroundColor:
                MaterialStateProperty.all<Color>(Colors.blue), // Button color
            foregroundColor:
                MaterialStateProperty.all<Color>(Colors.white), // Text color
            padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
                const EdgeInsets.symmetric(vertical: 16.0)), // Button padding
            shape: MaterialStateProperty.all<OutlinedBorder>(
              RoundedRectangleBorder(
                borderRadius:
                    BorderRadius.circular(8.0), // Button border radius
              ),
            ),
          ),
          child: Text(
            text,
            style: const TextStyle(fontSize: 24.0),
          ),
        ),
      ),
    );
  }

  /* Widget _buildBackspaceButton(String text) {
    return SizedBox(
      width: 80.0, // Fixed width for the backspace button
      child: ElevatedButton(
        onPressed: () => _onButtonPressed(text),
        style: ButtonStyle(
          backgroundColor:
              MaterialStateProperty.all<Color>(Colors.blue), // Button color
          foregroundColor:
              MaterialStateProperty.all<Color>(Colors.white), // Text color
          padding: MaterialStateProperty.all<EdgeInsetsGeometry>(
              const EdgeInsets.symmetric(vertical: 16.0)), // Button padding
          shape: MaterialStateProperty.all<OutlinedBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8.0), // Button border radius
            ),
          ),
        ),
        child: Text(
          text,
          style: const TextStyle(
              fontSize: 20.0), // Reduced font size for the backspace button
        ),
      ),
    );
  } */

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Integration Calculator'),
      ),
      body: Column(
        children: [
          // Function display area
          Expanded(
            child: GestureDetector(
              onTap: () {
                FocusScope.of(context).requestFocus(FocusNode());
              },
              child: Container(
                padding: const EdgeInsets.all(16.0),
                alignment: Alignment.bottomRight,
                child: TextField(
                  controller: _functionController,
                  onChanged: (value) {
                    setState(() {
                      _function = value;
                      _cursorPosition = _functionController.selection.baseOffset;
                    });
                  },
                  decoration: const InputDecoration(
                    border: InputBorder.none,
                    hintText: 'Enter function...',
                    contentPadding: EdgeInsets.zero,
                  ),
                  style: const TextStyle(fontSize: 24.0),
                ),
              ),
            ),
          ),
          // Display integration result
          _functionResult.isNotEmpty
              ? Text(
                  _functionResult,
                  style: const TextStyle(fontSize: 24.0),
                )
              : Container(),
          // Display graph
          _graphBase64.isNotEmpty
              ? Expanded(
                  child: Image.memory(
                    base64Decode(_graphBase64),
                    fit: BoxFit.contain,
                  ),
                )
              : Container(),
          const Divider(),
          // Calculator buttons
          Row(
            children: [
              _buildButton('('),
              _buildButton(')'),
              _buildButton('.'),
              _buildButton('C'),
              _buildButton('⌫'),
            ],
          ),
          Row(
            children: [
              _buildButton('sin'),
              _buildButton('cos'),
              _buildButton('tan'),
              _buildButton('cot'),
              _buildButton('^'),
            ],
          ),
          Row(
            children: [
              _buildButton('csc'),
              _buildButton('sec'),
              /*_buildButton('√'),*/
              _buildButton('/'),
              _buildButton('*'),
            ],
          ),
          Row(
            children: [
              _buildButton('7'),
              _buildButton('8'),
              _buildButton('9'),
              _buildButton('-'),
              _buildButton('+'),
            ],
          ),
          Row(
            children: [
              _buildButton('4'),
              _buildButton('5'),
              _buildButton('6'),
              _buildButton('x'),
              _buildButton('inv'),
            ],
          ),
          Row(
            children: [
              _buildButton('1'),
              _buildButton('2'),
              _buildButton('3'),
              _buildButton('0'),
              // _buildButton(''),
            ],
          ),
   
          Row(
            children: [
              _buildButton('e'),
              _buildButton('π'),
              _buildButton('inf'),
              _buildButton('ln'),
              _buildButton('='),
            ],
          ),
         
          // Inverse trigonometric function keys
          if (_showInverseKeys)
            Row(
              children: [
                _buildButton('asin'),
                _buildButton('acos'),
                _buildButton('atan'),
                _buildButton('acsc'),
                _buildButton('asec'),
                _buildButton('acot'),
              ],
            ),
        ],
      ),
    );
  }

  // Function for integration calculation
  Future<void> _integrate(
      String function, String lowerBound, String upperBound) async {
    final Map<String, dynamic> data = {
      'function': function,
      'lower_bound': lowerBound,
      'upper_bound': upperBound,
    };

    final Uri uri = Uri.parse('http://127.0.0.1:5000/integrate');

    final http.Response response = await http.post(
      uri,
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode(data),
    );

    final Map<String, dynamic> responseData = jsonDecode(response.body);

    if (response.statusCode == 200) {
      if (responseData.containsKey('result')) {
        // Display result and graph in dialog box
        _showResultDialog(
          'Result: ${responseData['result']}',
          responseData['graph'],
        );
      } else {
        // Display 'Not Defined' if result is not available
        setState(() {
          _functionResult = 'Result: Not Defined';
        });
      }
    } else {
      // Handle error here
      setState(() {
        _functionResult = 'Error: ${responseData['error']}';
      });
    }
  }

  // Function to show a dialog for entering bounds
  Future<void> _showBoundsDialog() async {
    String lowerBound = '';
    String upperBound = '';

    await showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Enter Lower and Upper Bounds'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Display the function for reference
              Text('Function: $_function'),
              TextField(
                onChanged: (value) {
                  lowerBound = value;
                },
                decoration: InputDecoration(labelText: 'Lower Bound'),
                keyboardType: TextInputType.number,
              ),
              TextField(
                onChanged: (value) {
                  upperBound = value;
                },
                decoration: InputDecoration(labelText: 'Upper Bound'),
                keyboardType: TextInputType.number,
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('Cancel'),
            ),
            TextButton(
              onPressed: () {
                // Call the integration function with bounds
                _integrate(_function, lowerBound, upperBound);
                Navigator.of(context).pop();
              },
              child: Text('OK'),
            ),
          ],
        );
      },
    );
  }

  // Function to show a dialog with the integration result and graph
  Future<void> _showResultDialog(String result, String graphBase64) async {
    await showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text('Integration Result'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Display the result
              Text(result),
              // Display the graph
              if (graphBase64.isNotEmpty)
                Image.memory(
                  base64Decode(graphBase64),
                  fit: BoxFit.contain,
                ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: Text('OK'),
            ),
          ],
        );
      },
    );
  }
}