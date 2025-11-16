# generate traffic light logic XML file for the ACO algorithm
def generate_pso_tls_logic(n_intersections, times):
    # assumes settings are in the 4 * 2 * 2 * 2 * 2
    # variety: each intersection has 64 total possible settings

    # pdb.set_trace()
    with open("data/cross.add.xml", "w") as logic:
        print('<additional>', file=logic)

        for i in range(times.shape[0]):
            tl_logic = f'<tlLogic id="{i + 1}" programID="stuff" ' + \
                'offset="0" type="static">'
            print(f'    {tl_logic}',
                  file=logic)

            if n_intersections == 1:
                # 16-character phase strings to match the 16 links created by netconvert (4 approaches * (Right, Straight, Left, U-turn))
                # Phase 1: E/W Straight + Right + U-turn Green
                print(f'         <phase duration="{times[i][0]}" state="rrrrGGgGrrrrGGgG" />', file=logic)
                # Phase 2: E/W Yellow
                print('         <phase duration="5" state="rrrryygyrrrryygy" />', file=logic)
                # Phase 3: E/W Left turn Green
                print(f'         <phase duration="{times[i][1]}" state="rrrrrrGrrrrrrrGr" />', file=logic)
                # Phase 4: E/W Left turn Yellow
                print('         <phase duration="5" state="rrrrrryrrrrrrryr" />', file=logic)
                # Phase 5: N/S Straight + Right + U-turn Green
                print(f'         <phase duration="{times[i][2]}" state="GGgGrrrrGGgGrrrr" />', file=logic)
                # Phase 6: N/S Yellow
                print('         <phase duration="5" state="yygyrrrryygyrrrr" />', file=logic)
                # Phase 7: N/S Left turn Green
                print(f'         <phase duration="{times[i][3]}" state="rrGrrrrrrrGrrrrr" />', file=logic)
                # Phase 8: N/S Left turn Yellow
                print('         <phase duration="5" state="rryrrrrrrryrrrrr" />', file=logic)
            else:
                # assume standard, four-way intersections; 8 possible light states
                strings = ["rrrGGgrrrGGg", "rrryygrrryyg",
                           "rrrrrGrrrrrG", "rrrrryrrrrry",
                           "GGgrrrGGgrrr", "yygrrryygrrr",
                           "rrGrrrrrGrrr", "rryrrrrryrrr"]

                # pdb.set_trace()
                for j in range(0, len(strings)//2):
                    print(f'         <phase duration="{times[i][j]}" ' +
                          f'state="{strings[j*2]}" />', file=logic)
                    print('         <phase duration="5" ' +
                          f'state="{strings[j*2+1]}" />',
                          file=logic)

            print("    </tlLogic>", file=logic)
        print("</additional>", file=logic)
