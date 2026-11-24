# Гнег · Война за архипелаг

Пошаговая морская стратегия на Python и Pygame. Развивайте экономику островов, расширяйте границы, стройте флот и уничтожьте столицу противника.

В главном меню можно начать партию против компьютера или сыграть вдвоём за одним ПК. В игре на двоих карта скрывается на время передачи хода. Текущая партия сохраняется автоматически и доступна через «Продолжить».

## Запуск

В готовой сборке Windows x64 распакуйте архив целиком и откройте **Gneg.exe**. Папка **_internal** должна оставаться рядом с приложением.

Для запуска из исходников используйте Python 3.12. Выполните команды из папки проекта.

```sh
python -m pip install -r requirements.txt
python main.py
```

## Первый ход

1. Справа выберите лесопилку и кликните по одной из подсвеченных клеток леса.
2. Выберите фрегат на карте. Голубые точки показывают, куда он может доплыть, красные углы отмечают цели в радиусе стрельбы.
3. Верфь уже построена. Во вкладке «Флот» можно заказать новый корабль и разместить его на свободной воде рядом с верфью.
4. Используйте до трёх действий и передайте ход. Доход поступает в начале следующего хода вашей стороны.

У каждого корабля по одному перемещению и залпу за ход. Башни стреляют автоматически в конце хода, форты прикрывают соседние здания. Для улучшений обычно нужны камень и золото, для III уровня также нужна платина.

| Управление | Действие |
| --- | --- |
| ЛКМ | Выбрать клетку, построить, переместиться или атаковать |
| ПКМ / Esc | Отменить выбор проекта |
| Пробел | Завершить ход |
| Tab | Выбрать следующий свой корабль |
| 1 / 2 / 3 | Переключить вкладку строительства |
| F1 | Открыть справку |
| Esc | Пауза или назад |
| M / F11 | Звук / полноэкранный режим |

## Исходники и сборка

- `gneg/game.py` — состояние партии, экономика и проверка действий.
- `gneg/catalog.py` — карта, типы объектов и баланс.
- `gneg/opponent.py` — компьютерный соперник.
- `gneg/app.py`, `gneg/interface.py` — управление и экраны.
- `gneg/storage.py` — автосохранение партии. В Windows файл хранится в `%LOCALAPPDATA%\Gneg\match.json`.

```sh
python -m unittest discover -s tests
```

Команды воспроизводят папку `dist\Gneg` на Windows x64 с установленными зависимостями:

```powershell
python -m pip install pyinstaller==6.22.3
python -m PyInstaller --noconfirm --windowed --name Gneg --icon assets/gneg.ico --add-data "assets;assets" --exclude-module numpy --exclude-module OpenGL main.py
```

Исходный проект — [Tmi-creator/Pygame_strategy](https://github.com/Tmi-creator/Pygame_strategy). Эта версия развивает механику исходной игры в одном приложении с новой зеркальной картой на 24 × 16 клеток. Иллюстрация главного меню сгенерирована в ImageGen. Шрифт Lato распространяется по SIL Open Font License, текст лицензии находится в `assets/Lato-OFL.txt`.

<details>
<summary>Запрос для иллюстрации главного меню</summary>

Create a gorgeous widescreen 16:9 landscape key art for an original Russian-language turn-based naval strategy game, no text whatsoever. Stylized illustrated strategy game key art, crisp shapes and finely painted texture, cohesive midnight navy, muted teal ocean, warm parchment and pale golden sun. High aerial perspective looking out over a rocky archipelago, with evergreen forests and a small weathered stone citadel on a large dramatic rocky island in the upper right; foreground right features a small fleet of two distinctive wooden sail ships, sails warm cream, foamy curving wakes. The left 43 percent is dark deep navy ocean with subtle illustrated wave lines and little detail, intentionally reserved for overlay UI including a game title and menu. Focus on the right two thirds with a depth gradient across the water and worldly natural lighting. Darker overall than a children's illustration, visually striking but hand-crafted, warm lights on the fort, evocative moody clouds in distance, no borders, no lettering, no symbols, no logos, no UI, no photograph. Island contours, blue-green sea and copper accent.

</details>
