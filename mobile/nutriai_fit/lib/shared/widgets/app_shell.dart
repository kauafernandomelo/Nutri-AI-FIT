import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../features/home/presentation/home_screen.dart';
import '../../features/meals/presentation/meals_screen.dart';
import '../../features/profile/presentation/profile_screen.dart';

/// Casca autenticada do app: navegação inferior entre Início/Refeições/Perfil,
/// com um FAB central que leva ao fluxo de registrar refeição.
///
/// As abas vivem em um IndexedStack (estado preservado ao trocar de aba). O
/// `/add-meal` é uma rota separada empilhada por cima — ao concluir, volta aqui.
class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  static const _tabs = [HomeScreen(), MealsScreen(), ProfileScreen()];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _index, children: _tabs),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.push('/add-meal'),
        tooltip: 'Registrar refeição',
        child: const Icon(Icons.add_a_photo),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(
              icon: Icon(Icons.home_outlined),
              selectedIcon: Icon(Icons.home),
              label: 'Início'),
          NavigationDestination(
              icon: Icon(Icons.restaurant_outlined),
              selectedIcon: Icon(Icons.restaurant),
              label: 'Refeições'),
          NavigationDestination(
              icon: Icon(Icons.person_outline),
              selectedIcon: Icon(Icons.person),
              label: 'Perfil'),
        ],
      ),
    );
  }
}
