import javax.security.sasl.SaslClient;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class PCY {

    public static void PCY(Integer br_kos, Double s, Integer br_pret, ArrayList<ArrayList<Integer>> kosare) throws IOException {

        Integer prag = Math.toIntExact(Math.round(Math.floor(s * br_kos)));

        HashMap<Integer, Integer> br_Pred = new HashMap<>();

        for(ArrayList<Integer> kosara : kosare){
            for(Integer predmet : kosara) {
               br_Pred.merge(predmet, 1, Integer::sum);
            }
        }
        int m = 0;
        for(Integer i: br_Pred.keySet()){
            if(br_Pred.get(i) >= prag) m++;
        }

        HashMap<Integer, Integer> pretinci = new HashMap<>();
        for(ArrayList<Integer> kosara : kosare){
            for(int i = 0; i < kosara.size(); i++) {
                int pred1 = kosara.get(i);
                int brPred1 = br_Pred.get(pred1);
                if(brPred1 < prag) continue;
                for(int j = i+1; j < kosara.size(); j++) {
                    int pred2 = kosara.get(j);
                    int brPred2 = br_Pred.get(pred2);
                    if(brPred1 >= prag && brPred2 >= prag){
                        int k = ((pred1*br_Pred.size()) + pred2) % br_pret;
                        pretinci.merge(k, 1, Integer::sum);
                    }
                }
            }
        }

        HashMap<String, Integer> parovi = new HashMap<>(br_pret);
        for(ArrayList<Integer> kosara : kosare){
            for(int i = 0; i < kosara.size(); i++) {
                int pred1 = kosara.get(i);
                int brPred1 = br_Pred.get(pred1);
                if(brPred1 < prag) continue;
                for(int j = i+1; j < kosara.size(); j++) {
                    int pred2 = kosara.get(j);
                    int brPred2 = br_Pred.get(pred2);
                    if(brPred1 >= prag && brPred2 >= prag){
                        int k = ((pred1*br_Pred.size()) + pred2) % br_pret;
                        if(pretinci.get(k) >= prag){
                            String kljuc = pred1 + " " + pred2;
                            parovi.merge(kljuc, 1, Integer::sum);
                        }
                    }
                }
            }
        }
        int A = m*(m-1)/2;
        System.out.println(A);
        System.out.println(parovi.size());

        List<Integer> vrijednosti = new ArrayList<>(parovi.values());

        Collections.sort(vrijednosti, Collections.reverseOrder());


       // try {
         //   FileWriter rezultati2 = new FileWriter("rezultati2.txt");
           // rezultati2.write(String.valueOf(A)+"\n");
            //rezultati2.write(String.valueOf(parovi.size())+"\n");
            for (int i = 0; i < vrijednosti.size(); i++) {
                int vr = vrijednosti.get(i);
                if(vr >= prag) {
                    System.out.println(vr);
              //      rezultati2.write(String.valueOf(vrijednosti.get(i)) + "\n");
                }
            }
           // rezultati2.close();
       // }catch (IOException e){
        //}


    }
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);
        List<String> lines = new ArrayList<>();
        int j = 0;
        Integer N = 0;
        Double s = 0.0;
        Integer b = 0;
        float start = System.nanoTime();
        while(scanner.hasNextLine()){
            String line = scanner.nextLine().trim();
            if(!line.equals("EOF") && !line.isEmpty()) {
                if (j == 0) N = Integer.parseInt(line);
                else if (j == 1) s = Double.parseDouble(line);
                else if (j == 2) b = Integer.parseInt(line);
                else lines.add(line);
                j++;
            }
            else break;
        }

        ArrayList<ArrayList<Integer>> kosare = new ArrayList<>(N);

        for(String line: lines){
            String[] nizPr = line.split(" ");
            ArrayList<Integer> pred = new ArrayList<>(nizPr.length);
            for(int i = 0; i < nizPr.length; i++){
                pred.add(Integer.parseInt(nizPr[i]));
            }
            kosare.add(pred);
        }

        try {
            PCY(N, s, b, kosare);
        }catch (IOException e)
        {}

        System.err.println((System.nanoTime() - start) / Math.pow(10, 9));


    }
}
