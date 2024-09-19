import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';

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
      duration: const Duration(seconds: 5),
      vsync: this,
    );

    _animation = Tween<Offset>(
      begin: Offset(150, 250), // Center of the rectangle
      end: _endPoint,
    ).animate(_controller);

    _controller.repeat(reverse: true);

    _timer = Timer.periodic(Duration(seconds: 5), (timer) {
      _fetchCoordinates();
    });
  }

  Future<void> _fetchCoordinates() async {
    final response = await http.get(Uri.parse('YOUR_API_ENDPOINT_HERE'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['users'] != null && data['users'].isNotEmpty) {
        final user = data['users'][0];
        if (user['position'] != null) {
          setState(() {
            _endPoint = Offset(user['position']['x'], user['position']['y']);
            _animation = Tween<Offset>(
              begin: _animation.value,
              end: _endPoint,
            ).animate(_controller);
            _controller.forward(from: 0);
          });
        }
      }
    } else {
      throw Exception('Failed to load coordinates');
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
                      color: Colors.red,
                      shape: BoxShape.circle,
                    ),
                  ),
                );
              },
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RedDotAnimation()),
                );
              },
              child: Text('Go to Red Dot Page'),
            )
          ],
        ),
      ),
    );
  }
}
