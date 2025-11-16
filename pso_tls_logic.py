# generate traffic light logic XML file for the ACO algorithm
def generate_pso_tls_logic(times):
    # assumes settings are in the 4 * 2 * 2 * 2 * 2
    # variety: each intersection has 64 total possible settings

    # pdb.set_trace()
    with open("data/cross.add.xml", "w") as logic:
        print('<additional>', file=logic)

        # assume standard, four-way intersections; 8 possible light states
        strings = ["rrrGGgrrrGGg", "rrryygrrryyg",
                   "rrrrrGrrrrrG", "rrrrryrrrrry",
                   "GGgrrrGGgrrr", "yygrrryygrrr",
                   "rrGrrrrrGrrr", "rryrrrrryrrr"]

        for i in range(times.shape[0]):
            tl_logic = f'<tlLogic id="{i + 1}" programID="stuff" ' + \
                'offset="0" type="static">'
            print(f'    {tl_logic}',
                  file=logic)

            # pdb.set_trace()
            for j in range(0, len(strings)//2):
                print(f'         <phase duration="{times[i][j]}" ' +
                      f'state="{strings[j*2]}" />', file=logic)
                print('         <phase duration="5" ' +
                      f'state="{strings[j*2+1]}" />',
                      file=logic)

            print("    </tlLogic>", file=logic)
        print("</additional>", file=logic)
