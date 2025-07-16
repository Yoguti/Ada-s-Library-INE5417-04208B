#include <iostream>
#include <mutex>
#include <stdlib.h>
#include <thread>
#include <type_traits>
// Interleaved Character Printing #1
void functionsymbolone(char symbol) {
  for (int i = 0; i < 100; i++) {
    std::cout << symbol;
  }
}

void functionsymboltwo(char symbol2) {
  for (int i = 0; i < 100; i++) {
    std::cout << symbol2;
  }
}

void exec_one() {
  char symbol;
  char symbol2;

  std::cout << "Enter first symbol: ";
  std::cin >> symbol;

  std::cout << "Enter second symbol: ";
  std::cin >> symbol2;

  std::thread first_symbol(functionsymbolone, symbol);
  std::thread second_symbol(functionsymboltwo, symbol2);

  first_symbol.join();
  second_symbol.join();
}

// Ping Pong with Mutex
std::mutex mut;
bool pingTurn = true;

void ping() {
  for (int i = 0; i < 10; i++) {
    while (true) {
      mut.lock();
      if (pingTurn) {
        std::cout << "Ping\n";
        pingTurn = false;
        mut.unlock();
        break;
      }
      mut.unlock();
      std::this_thread::yield();
    }
  }
}
void pong() {
  for (int i = 0; i < 10; i++) {
    while (true) {
      mut.lock();
      if (!pingTurn) {
        std::cout << "Pong\n";
        pingTurn = true;
        mut.unlock();
        break;
      }
      mut.unlock();
      std::this_thread::yield();
    }
  }
}

void exec_two() {
  std::thread work_ping(ping);
  std::thread work_pong(pong);

  work_ping.join();
  work_pong.join();
}

int main() {
  //  exec_one();
  exec_two();
  return 0;
}
