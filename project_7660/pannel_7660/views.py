from django.shortcuts import render
from pannel_7660.function.functions import MyThread
from pannel_7660.function.functions import MyThread1
from pannel_7660.function.functions import MyThread2

def main_page(request):

#     setups = """
#     BEJSRTL442
# BEJSRTL392
# BEJSRTL717
# BEJSRTL738
# BEJSRTL688
# BEJSRTL749
# BEJSRTL659
# BEJSRTL807
# BEJSRTL853
# BEJSRTL854
# BEJSRTL166
# BEJSRTL675
# BEJSRTL436
# BEJSRTL629
# BEJSRTL402
# BEJSRTL473
# BEJSRTL701
# BEJSRTL846
# BEJSRTL847
# BEJSRTL679
# BEJSRTL840
# BEJSRTL753
# BEJSRTL684
# BEJSRTL674
# BEJSRTL765
# BEJSRTL627
# BEJSRTL848
# BEJSRTL849
# BEJSRTL851
# BEJSRTL852
# BEJSRTL635
# BEJSRTL616
# BEJSRTL157
# BEJSRTL122
# BEJSRTL479
# BEJSRTL482
# BEJSRTL666
# BEJSRTL841
# BEJSRTL167
# BEJSRTL168
# BEJSRTL724
# BEJSRTL655
# BEJSRTL667
# BEJSRTL859
# BEJSRTL663
# BEJSRTL662
# BEJSRTL668
# BEJSRTL661
# BEJSRTL808
# BEJSRTL712
# BEJSRTL715
# BEJSRTL809
# BEJSRTL857
# BEJSRTL858
# BEJSRTL781
# BEJSRTL644
# BEJSRTL806
# BEJSRTL855
# BEJSRTL856
# BEJSRTL372
# BEJSRTL437
# BEJSRTL438
# BEJSRTL230
# BEJSRTL643
# BEJSRTL434
# BEJSRTL477
# BEJSRTL827
# BEJSRTL653
# BEJSRTL820
# BEJSRTL610
# BEJSRTL844
# BEJSRTL652
# BEJSRTL804
# BEJSRTL824
# BEJSRTL805
# BEJSRTL815
# BEJSRTL845
# BEJSRTL214
# BEJSRTL814
# BEJSRTL470
# BEJSRTL656
# BEJSRTL665
# BEJSRTL689
# BEJSRTL826
# BEJSRTL723
# BEJSRTL816
# BEJSRTL812
# BEJSRTL676
# BEJSRTL622
# BEJSRTL249
# BEJSRTL654
# BEJSRTL713
# BEJSRTL198
# BEJSRTL692
# BEJSRTL630
# BEJSRTL261
# BEJSRTL731
# BEJSRTL762
# BEJSRTL830
# BEJSRTL834
# BEJSRTL831
# BEJSRTL175
# BEJSRTL832
# BEJSRTL207
# BEJSRTL838
# BEJSRTL833
# BEJSRTL743
# """
    setups = """BEJSRTL505
BEJSRTL468
BEJSRTL795
BEJSRTL364
BEJSRTL768
"""
    inf = {}
    setups_list = setups.strip().split()
    t_list = []

    for j in range(0, len(setups_list)):
        try:
            thread1 = MyThread(setups_list[j])
        except IndexError:
            pass
        else:
            thread1.start()
            t_list.append(thread1)
    for t in t_list:
        t.join()
    for t in t_list:
        inf[t_list.index(t)] = t.get_result()
    return render(request, 'main_page.html', {'inf_dict': inf})


def msim(request):
    setups_1 = """
    BEJSRTL442


BEJSRTL392

BEJSRTL738

BEJSRTL688

BEJSRTL749

BEJSRTL659 

BEJSRTL807

BEJSRTL853

BEJSRTL854

BEJSRTL166

BEJSRTL675

BEJSRTL436

BEJSRTL629

BEJSRTL402

BEJSRTL473

BEJSRTL701

BEJSRTL846

BEJSRTL847

BEJSRTL679

BEJSRTL840

BEJSRTL753

BEJSRTL684

BEJSRTL674

BEJSRTL765

BEJSRTL627

BEJSRTL848

BEJSRTL849

BEJSRTL851

BEJSRTL676

BEJSRTL635

BEJSRTL616

BEJSRTL157

BEJSRTL122

BEJSRTL479

BEJSRTL482

BEJSRTL666

BEJSRTL841

BEJSRTL167

BEJSRTL168

BEJSRTL724

BEJSRTL655

BEJSRTL667

BEJSRTL859

BEJSRTL663

BEJSRTL662

BEJSRTL668

BEJSRTL661

BEJSRTL808

BEJSRTL715

BEJSRTL809

BEJSRTL857

BEJSRTL781

BEJSRTL644

BEJSRTL806

BEJSRTL855

BEJSRTL856

BEJSRTL372

BEJSRTL437

BEJSRTL438

BEJSRTL722

BEJSRTL643


    """
    setups_2 = """
 BEJSRTL434
BEJSRTL717
BEJSRTL477
BEJSRTL827
BEJSRTL653
BEJSRTL820
BEJSRTL622
BEJSRTL610
BEJSRTL844
BEJSRTL652
BEJSRTL804
BEJSRTL198
BEJSRTL824
BEJSRTL805
BEJSRTL815
BEJSRTL845
BEJSRTL422

"""
    setups_3 = """
    BEJSRTL470
BEJSRTL656
BEJSRTL665
BEJSRTL731
BEJSRTL762
BEJSRTL654
BEJSRTL713
BEJSRTL689
BEJSRTL852
BEJSRTL249
BEJSRTL261
BEJSRTL712
BEJSRTL630
BEJSRTL826
BEJSRTL692
BEJSRTL723
BEJSRTL816
BEJSRTL858
BEJSRTL812
BEJSRTL814

"""
    sus = """
    BEJSRTL831
BEJSRTL832
BEJSRTL834
BEJSRTL833
BEJSRTL175
BEJSRTL207
BEJSRTL838
BEJSRTL743

"""
    MK5 = """
"""
    inf = {}
    setups_list_1 = setups_1.strip().split()
    setups_list_2 = setups_2.strip().split()
    setups_list_3 = setups_3.strip().split()
    sus = sus.strip().split()
    MK5 = MK5.strip().split()
    track_setup = {'section': ['Track-1', 'Track-2', 'Track-3', 'SUS', 'MK5'],
                   'setup_infor': [setups_list_1, setups_list_2, setups_list_3, sus, MK5]}
    t_list = []
    for i in range(0, 5):
        for j in range(0, len(track_setup['setup_infor'][i])):
            try:
                thread1 = MyThread1(track_setup['section'][i], track_setup['setup_infor'][i][j])
            except IndexError:
                pass
            else:
                thread1.start()
                t_list.append(thread1)
    for t in t_list:
        t.join()
    for t in t_list:
        inf[t_list.index(t)] = t.get_result()
    return render(request, 'MSIM.html', {'inf_dict': inf})
    # return HttpResponse(b'ok')


def ssim(request):
    setups_1 = """
        BEJSRTL819
BEJSRTL709
BEJSRTL730
BEJSRTL772
BEJSRTL861
BEJSRTL862
BEJSRTL863
BEJSRTL864
BEJSRTL865
BEJSRTL170
BEJSRTL275
BEJSRTL823
BEJSRTL774
BEJSRTL286
BEJSRTL405
BEJSRTL512
BEJSRTL631
BEJSRTL828
BEJSRTL741
BEJSRTL739
BEJSRTL860
BEJSRTL729
BEJSRTL799
BEJSRTL801
BEJSRTL843
BEJSRTL683
BEJSRTL626
BEJSRTL489
BEJSRTL365
BEJSRTL221
BEJSRTL513
BEJSRTL677
BEJSRTL695
BEJSRTL705
BEJSRTL726
BEJSRTL757
BEJSRTL490
BEJSRTL782
BEJSRTL810
BEJSRTL623
BEJSRTL609
BEJSRTL619
BEJSRTL850
BEJSRTL636
BEJSRTL680
BEJSRTL681
BEJSRTL693
BEJSRTL710
BEJSRTL608
BEJSRTL682
BEJSRTL790
BEJSRTL822
BEJSRTL696
BEJSRTL698
BEJSRTL699
BEJSRTL501
BEJSRTL811
BEJSRTL842
        """
    setups_2 = """BEJSRTL825
BEJSRTL697
BEJSRTL702
BEJSRTL778
BEJSRTL601
BEJSRTL813
BEJSRTL615
BEJSRTL802
BEJSRTL791
BEJSRTL704
BEJSRTL745
BEJSRTL714
BEJSRTL624
BEJSRTL780
BEJSRTL700"""
    setups_3 = """
    BEJSRTL773
BEJSRTL735
BEJSRTL775
BEJSRTL727
BEJSRTL720 
BEJSRTL650
BEJSRTL647
BEJSRTL642
BEJSRTL750
BEJSRTL797
BEJSRTL327
BEJSRTL022
BEJSRTL605
BEJSRTL788
BEJSRTL736
    """
    sus = """
    BEJSRTL836
BEJSRTL835
BEJSRTL837
    """
    inf = {}
    setups_list_1 = setups_1.strip().split()
    setups_list_2 = setups_2.strip().split()
    setups_list_3 = setups_3.strip().split()
    sus = sus.strip().split()
    track_setup = {'section': ['Track-1', 'Track-2', 'Track-3', 'SUS'],
                   'setup_infor': [setups_list_1, setups_list_2, setups_list_3, sus]}
    t_list = []
    for i in range(0, 4):
        for j in range(0, len(track_setup['setup_infor'][i])):
            try:
                thread1 = MyThread1(track_setup['section'][i], track_setup['setup_infor'][i][j])
            except IndexError:
                pass
            else:
                thread1.start()
                t_list.append(thread1)
    for t in t_list:
        t.join()
    for t in t_list:
        inf[t_list.index(t)] = t.get_result()
        print(inf)
    return render(request, 'SSIM.html', {'inf_dict': inf})
    # return HttpResponse(b'ok')


def mac(request):
    mac = """7660utt001smini
bejsrtm022smini
bejsrtm002smini
bejsrtm001smini
bejsrtm009smini
bejsrtm005smini
7560utt009smini
bejsrtm015smini
7560utt127smini
7560utt236smini
bejsrtm010smini
bejsrtm011smini
bejsrtm020smini
7560utt241smini
bejsrtm003smini
bejsrtm008smini
7560utt014smini
ice7360-mini
bejsrtm014smini
bejsrtm024smini
bejsrtm017
bejsrtm016
bejsrtm018smini
bejsrtm021smini
bejsrtm023smini
7560utt243smini
bejsrtm052smini
bejsrtm061smini
bejsrtm065smini
bejsrtm034smini
bejsrtm038smini
bejsrtm037smini
bejsrtm049smini
bejsrtm066smini
bejsrtm069smini
bejsrtm047smini
bejsrtm060smini
7560utt011smini
bejsrtm073smini
7560-utt-000
bejsrtm028smini
bejsrtm067smini
bejsrtm074smini
bejsrtm063smini
bejsrtm048smini
bejsrtm041smini
bejsrtm058smini
bejsrtm075smini
bejsrtm064smini
bejsrtm035smini
bejsrtm026smini
bejsrtm044smini
bejsrtm045smini
bejsrtm043smini
bejsrtm039smini
bejsrtm046
bejsrtm027smini
bejsrtm050smini
bejsrtm031smini
bejsrtm062smini
bejsrtm053smini
bejsrtm059smini
bejsrtm042smini
bejsrtm030smini
bejsrtm051smini
bejsrtm055smini
bejsrtm057smini
bejsrtm036smini
bejsrtm056smini
bejsrtm054smini
bejsrtm040smini
bejsrtm033smini
bejsrtm032smini
bejsrtm029smini
bejsrtm068smini
bejsrtm070smini
bejsrtm071smini
bejsrtm072smini"""
    mac_list = mac.split()
    t_list = []
    inf = {}
    for k in range(0, len(mac_list)):
        try:
            thread1 = MyThread2(mac_list[k])
        except IndexError:
            pass
        else:
            thread1.start()
            t_list.append(thread1)
    for t in t_list:
        t.join()
    for t in t_list:
        inf[t.get_mac()] = t.get_result()
    return render(request, 'Linux_PC.html', {'inf_dict': inf})

