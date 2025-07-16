#include <mutex>
#include <thread>
#include <vector>

void sum_array(std::vector<int> &vec) {
  int acc = 0;

  for (int i = 0; i < vec.size(); i++) {
    acc += vec.at(i);
  }
}

int main() {
  std::vector<int> original = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
  int chunkSize = 4;

  std::vector<int> part1(original.begin(), original.begin() + chunkSize);
  std::vector<int> part2(original.begin() + chunkSize,
                         original.begin() + 2 * chunkSize);
  std::vector<int> part3(original.begin() + 2 * chunkSize, original.end());

  std::thread work1(sum_array, part1);
  std::thread work2(sum_array, part2);
  std::thread work3(sum_array, part3);
}
