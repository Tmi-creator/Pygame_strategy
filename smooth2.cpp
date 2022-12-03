#include <bits/stdc++.h>

std::vector <std::vector <int>> func(std::vector <std::vector <int>> b, std::vector<int> poses, int ggg, std::vector <std::vector <int>> bar){
    int zzz = 0;
    if(b[0][4] == 0 && b[4][0] != 0) zzz = 1;
    int yyy = 0;
    if (b[0][4] == 0 && b[4][0] == 0) yyy = 1;
    int fff[2];
    // int ab = abs(b[0][4] - 1);
    // int ba = abs(b[4][0] - 1);
    // if(ba != ab) ab = ba;
    int c = abs(poses[4] - poses[0]) - 1; //balbes rabotai uzhe
    int cc = c;
    if (c < 1) c = 2;
    if (b[0][2] < b[4][2] && b[2][0] < b[2][4]) {
        fff[0] = b[0][0];
        fff[1] = b[4][4];
        for(int i = 1; i < 7 - c; i++) {
            for (int o = c; o > i - 1; o--) {
                //std::cout<<"durak" << '\n';
                if (4 - i > -1) b[o + zzz][4 - i] = fff[ggg]; //+ab - ba
                //b[o + 1 - b[4][0] - b[4][2] + b[4][1] + zzz][4 - i] = fff[ggg]; //+ab - ba
                //if (4 - i > -1) b[o - (b[4][0] == b[4][4]) + (b[4][1] == b[4][4]) + zzz][4 - i] = fff[ggg]; //+ab - ba

                }
        }
        //00001
        //00001
        //00001
        //00001
        //11111

    } else if (b[0][2] < b[4][2] && b[2][0] > b[2][4]) {
        fff[0] = b[0][4];
        fff[1] = b[4][0];
        if (cc < 1) c = 1;
        for(int i = 1; i < 8 - c; i++) {
            for (int o = c + 1; o < i + 2; o++) {
                b[i - zzz][o - 2*zzz] = fff[ggg]; //-ab + ba
                // b[i - 1 + b[4][0] + b[4][2] - b[4][1] - zzz][o - 2*zzz] = fff[ggg]; //-ab + ba
        //10000
        //10000
        //10000
        //10000
        //11111
        for(int i = 0; i < 5; i++){
            b[4][i] = bar[4][i];
            b[i][0] = bar[i][0];
        }
                    // if (o != poses[4] + i)
                //     b[poses[4] + i][o]++;
                }
            }
    } else if(b[0][2] > b[4][2] && b[2][0] > b[2][4]) {
        fff[0] = b[4][4];
        fff[1] = b[0][0];
        for(int i = 7 - c; i > 0; i--) {
            for (int o = c; o < i + c - 1; o++) {
                //if (-1 < o - 2 + abs(!(b[0][0]) - 1) - abs(!(b[0][4]) - 1) - zzz - yyy < 5 && -1 < 6 - i - abs(!(b[0][0]) - 1) + abs(!(b[4][0]) - 1) - zzz < 5) {
                    //b[o - 2 + (b[4][0] == b[3][0]) - (b[0][4] == b[0][3]) - zzz - yyy][6 - i - (b[4][0] == b[3][0]) + (b[4][0] == b[3][0]) - zzz] = fff[ggg];

                //b[o - 2 + b[0][0] - b[0][4] - zzz - yyy][6 - i - b[0][0] + b[4][0] - zzz] = fff[ggg];
                ////if (-1 < o - 2 - zzz - yyy && o - 2 - zzz - yyy < 5 &&  -1 < 6 - i - zzz && 6 - i - zzz < 5) b[o - 2 - zzz - yyy][6 - i - zzz] = fff[ggg];

                //}
            }
        }
        //22222
        //21111
        //21111
        //21111
        //21111
        for(int i = 0; i < 5; i++){
            b[0][i] = bar[0][i];
            b[i][0] = bar[i][0];
            b[4][i] = bar[4][i];
            b[i][4] = bar[i][4];
        }
    } else if(b[0][2] > b[4][2] && b[2][0] < b[2][4]) {
        fff[0] = b[4][0];
        fff[1] = b[0][4];
        for(int i = 7 - c; i > 0; i--) {
            for (int o = c; o > i - c; o--) {
                b[i - 1][o + 1] = fff[ggg];
            }
        }
        //11111
        //00001
        //00001
        //00001
        //00001
        for(int i = 0; i < 5; i++){
            b[0][i] = bar[0][i];
            b[i][0] = bar[i][0];
            b[4][i] = bar[4][i];
            b[i][4] = bar[i][4];
       }
    }
    return b;
}

int main() {
    std::string s;
    std::ifstream fout;
    fout.open("input.txt");
    std::string a[40];

    for(int i = 0; i < 40; i++) {
        fout>>s;
        a[i] = s;
    }
    fout.close();
    for(int k = 0; k < 35; k++) {
        for(int l = 0; l < 35; l++) {
            std::vector <std::vector <int>> b(40, std::vector<int>(40, 0));
            for(int i = 0; i < 5; i++) {
                for(int j = 0; j < 5; j++){
                    b[i][j] = a[k + i][l + j] - '0';
                    // int b = a[j][i] - '0';
                    // int c = a[j][i + 1] - '0';

                }
            }

            double sr = 0;
            for(int i = 0; i < 5; i++) {
                for(int j = 0; j < 5; j++){
                    if(b[i][j] != 0)
                        sr++;
                }
            }
            sr /= 25;
            if(sr == int(sr) || sr < 0.6){
                continue;
            }
    // int b[5][5] = { {3, 2, 3, 2, 3},
    //                 {2, 2, 2, 2, 3},
    //                 {2, 3, 2, 2, 2},
    //                 {3, 3, 2, 2, 3},
    //                 {2, 2, 3, 2, 2} };
            std::vector <std::vector <int>> bar(5, std::vector<int>(5, 0));
            for(int i = 0; i < 5; i++) {
                for(int j = 0; j < 5; j++) {
                    bar[i][j] = b[i][j];
                }
            }

            std::vector<int> poses(5, 0);
            int cnt[40];
            // int pos = 0;
            bool tr = true;
            for (int j = 0; j < 5; j++) {
                int prev = b[j][0];
                int cur;

                for (int i = 1; i < 5; i++) {
                    cur = b[j][i];
                    if (prev != cur){
                        //pos = i;
                        poses[j] = i;
                        tr = false;
                        //break;// Использовать еще раз
                    }
                    prev = cur;
                }

                if(tr) poses[j] = 0;
                tr = true;
                cnt[poses[j]]++;
                //01004
            }
            bool fls = false;
            bool brk = false;
            for(int i = 0; i < 5; i++){
                if(cnt[i] > 2 && cnt[i] != 5){
                    // pos = i;
                    std::cout << "works\n";
                    brk = true;
                    break;
                }
                if(i == 4) fls = true;
            }
            // if (brk) {
            //     brk = false;
            //     break;
            // }
            if(!fls){
                b = func(b, poses, 1, bar);
                if(l % 2 == 0) b = func(b, poses, 0, bar);
                }
            for(int i = 0; i < 5; i++) {
                for(int j = 0; j < 5; j++){
                    a[k + i][l + j] = b[i][j] + '0';
                }
            }
            std::cout << k << ' ' << l << '\n';

        }
        std::ofstream fou;
        fou.open("output.txt");
        for (int i = 0; i < 40; i++) {
            fou << a[i];
            fou << "\n";
        }
    }

    std::ofstream fou;
    fou.open("output.txt");
    for (int i = 0; i < 40; i++) {
        fou << a[i];
        fou << "\n";
    }
    // for(int i = 0; i < 5; i++){
    //     for(int j = 0; j <5; j++){
    //         cout << b[i][j];
    //     }
    //     cout << endl;

}

// 10000        11111
// 10000        00001
// 10000        00001
// 10000        00001
// 11111        00001

// проверка на 0 (0 -> 1)
//
// 00001        00001       01111
// 00011        00001       01111
// 00101        00001       01111
// 01001        00001       01111
// 11111        11111       00000

