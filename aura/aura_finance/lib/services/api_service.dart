import 'dart:convert';
import 'dart:io' show Platform;
import 'package:http/http.dart' as http;

class ApiService {
  // Use 10.0.2.2 for Android emulator to connect to host's localhost.
  // For iOS simulator and other platforms, localhost/127.0.0.1 is fine.
  static String get _backendBaseUrl {
    // Use 10.0.2.2 for Android emulator to connect to host's localhost.
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000'; // TODO: Replace with your local server port.
    }
    // For iOS simulator and other platforms, localhost/127.0.0.1 is fine.
    return 'http://127.0.0.1:8000'; // TODO: Replace with your local server port.
  }

  static String get _backendUrl => '$_backendBaseUrl/chat';

  static Future<String> sendMessage(String message) async {
    try {
      final response = await http.post(
        Uri.parse(_backendUrl),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'message': message,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        print(data['response']);
        return data['response'] ?? 'Sorry, I could not understand that.';
      } else {
        return 'Error: ${response.statusCode}';
      }
    } catch (e) {
      // It's helpful to see the actual error during development.
      return 'Error: Could not connect to the server. $e';
    }
  }
}