// import 'dart:nativewrappers/_internal/vm/lib/internal_patch.dart';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'dart:math';
// import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'dart:developer';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
  BluetoothService().startScan();
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Page'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => RedDotAnimation()),
            );
          },
          child: Text('Go to Red Dot Page'),
        ),
      ),
    );
  }
}

class SecondPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Home Page'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => RedDotAnimation()),
            );
          },
          child: Text('Go to Red Dot Page'),
        ),
      ),
    );
  }
}

class RedDotAnimation extends StatefulWidget {
  @override
  _RedDotAnimationState createState() => _RedDotAnimationState();
}

class _RedDotAnimationState extends State<RedDotAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _animation;
  late Timer _timer;
  Offset _endPoint = Offset(150, 250); // Center of the rectangle
  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 1),
      vsync: this,
    );

    _animation = Tween<Offset>(
      begin: Offset(150, 250), // Center of the rectangle
      end: _endPoint,
    ).animate(_controller);

    _controller.repeat(reverse: true);

    _timer = Timer.periodic(Duration(seconds: 1), (timer) {
      _fetchCoordinates();
    });
  }

  Future<void> _fetchCoordinates() async {
    final response = await http
        .get(Uri.parse('https://maradeursmap.iw.goncharov.page/users'));
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      if (data['users'] != null && data['users'].isNotEmpty) {
        final user = data['users'][0];
        if (user['position'] != null) {
          // print('${user['position']['x'].runtimeType}');
          // print('${(user['position']['x'] * 100000).round().runtimeType}');
          print('${(user['position']['x'] * 100000).round() % 10 * 3 + 150}');
          setState(() {
            _endPoint = Offset(
                (((user['position']['x'] * 100000).round() % 10) * 10 + 150)
                    .toDouble(),
                (((user['position']['y'] * 100000).round() % 10) * 20 + 250)
                    .toDouble());
            // (user['position']['x'] - 37) * 100, // 1 meter = 10

            // (user['position']['y'] - 55) * 100); // 1 meter = 10
            _animation = Tween<Offset>(
              begin: _animation.value,
              end: _endPoint,
            ).animate(_controller);
            _controller.forward(from: 0);
          });
        }
      }
    } else {
      // throw Exception('Failed to load coordinates ${response.statusCode}');
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        width: 300,
        height: 500,
        color: Colors.grey[300],
        child: Stack(
          children: [
            SvgPicture.asset(
              'assets/Бантик.svg', // Replace with your SVG asset path
              width: 300,
              height: 500,
              fit: BoxFit.cover,
            ),
            AnimatedBuilder(
              animation: _animation,
              builder: (context, child) {
                return Positioned(
                  left: _animation.value.dx,
                  top: _animation.value.dy,
                  child: Container(
                    width: 10,
                    height: 10,
                    decoration: BoxDecoration(
                      color: const Color.fromARGB(255, 147, 42, 34),
                      shape: BoxShape.circle,
                    ),
                  ),
                );
              },
            ),
            // ElevatedButton(
            //   onPressed: () {
            //     Navigator.push(
            //       context,
            //       MaterialPageRoute(builder: (context) => RedDotAnimation()),
            //     );
            //   },
            //   child: Text('Go to Red Dot Page'),
            // )
          ],
        ),
      ),
    );
  }
}

class BluetoothService {
  List<BluetoothDevice> devicesList = [];

  void startScan() {
    FlutterBluePlus.startScan(timeout: Duration(seconds: 1));

    FlutterBluePlus.scanResults.listen((results) {
      for (ScanResult r in results) {
        if (!devicesList.contains(r.device)) {
          devicesList.add(r.device);
          connectToDevice(r.device);
        }
      }
    });

    // Restart scan after a delay to continuously scan
    Future.delayed(Duration(seconds: 5), () {
      FlutterBluePlus.stopScan();
      startScan();
    });
  }

  void connectToDevice(BluetoothDevice device) async {
    await device.connect();
    // Add more logic here to interact with the connected device
  }
}
