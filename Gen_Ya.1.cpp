#include <bits/stdc++.h>

using namespace std;


void func2(int start_x, int start_y, std::vector <std::vector <int>> &a) {
        int n = 2;
        if(rand() % 3 == 0) {
            n++;
            if(rand() % 3 == 0) n++;
        }
        int bebebe, bababa;
        for (int j = 0; j < n; j++) {
            if (rand() % 2 == 0) {
                bebebe = start_x + rand() % 4;
            } else {
                bebebe = start_x - rand() % 4;
            }

            if (rand() % 2 == 0) {
                bababa = start_y + rand() % 4;

            } else {
                bababa = start_y - rand() % 4;
            }

            int end_x, end_y;

            if (rand() % 2 == 0) {
                end_x = bebebe + 3 + rand() % 2;
            } else {
                end_x = bebebe - 3 - rand() % 2;
            }

            if (rand() % 2 == 0) {
                end_y = bababa + 3 + rand() % 2;

            } else {
                end_y = bababa - 3 - rand() % 2;
            }

            for (int l = std::min(bebebe, end_x); l < std::max(bebebe, end_x); l++) {
                for (int k = std::min(bababa, end_y); k < std::max(bababa, end_y); k++) {
                    a[l][k] = 0;
                }
            }
        }
}

void func(int start_x, int start_y, std::vector <std::vector <int>> &a) {
        int n = 13;
        for (int j = 0; j < n; j++) {
            int end_x, end_y;

            if (rand() % 2 == 0) {
                end_x = start_x + rand() % 8;
            } else {
                end_x = start_x - rand() % 8;
            }

            if (rand() % 2 == 0) {
                end_y = start_y + rand() % 8;

            } else {
                end_y = start_y - rand() % 8;
            }

            for (int l = std::min(start_x, end_x); l < std::max(start_x, end_x); l++) {
                for (int k = std::min(start_y, end_y); k < std::max(start_y, end_y); k++) {
                    if(rand() % 6 == 0){
                        a[l][k]++;
                    }
                    a[l][k]++;
                }
            }
        }
        func2(start_x, start_y, a);
}



int main() {

    srand(time(NULL));
    int x = 40, y = 40, cnt = 0;
    vector<vector<int>> a(x, vector<int> (y, 0));
    int p = 1;

//vector<vector<int>> t(100, vector<int> (100, 0);

    ofstream fout;
    fout.open("input.txt");
    for(int d = 0; d < 2; d++){
    for (int i = 1; i < 3; i++) {
        int start_x = i * i * 8;
        int start_y = p * p * 8;

        func(start_x, start_y, a);
    }p++;
}

func(20, 20, a);





    for (int i = 0; i < 40; i++) {
        for (int j = 0; j < 40; j++) {
            fout << a[j][i];
        }
        fout << "\n";
    }



}