import java.util.*;

public class EVCalculator { 
    // Convert American odds to decimal 
    public static double convertOddsToDecimal(int americanOdds) { 
        if (americanOdds > 0) {
            return 1.0 + (americanOdds / 100.0);
        } else if (americanOdds < 0) {
            return 1.0 + (100.0 / Math.abs(americanOdds));
        } else {
            throw new IllegalArgumentException("Odds cannot be zero");
        }
    }

    // Calculate implied probability 
    public static double impliedProbability(double decimalOdds) { 
        return 1.0 / decimalOdds; 
    }

    // Calculate total implied probability 
    public static double totalImpliedProbability(double over, double under) { 
        return over + under; 
    }

    // Calculate market juice 
    public static double marketJuice(double totalImplied) { 
        return totalImplied - 1.0; 
    }

    // Expected Value (EV) calculation 
    public static double EVCalculation(double fairValue, double finalOdds) { 
        return (fairValue * finalOdds) - (1 - fairValue); 
    }

    // Calculate fair value, market juice, and EV percentage
    public static double[] calculateFairValue(int over, int under, int finalOdds) {
        double overDecimal = convertOddsToDecimal(over);
        double underDecimal = convertOddsToDecimal(under);
        double finalDecimal = convertOddsToDecimal(finalOdds) - 1.0;

        double overImplied = impliedProbability(overDecimal);
        double underImplied = impliedProbability(underDecimal);
        double totalImplied = totalImpliedProbability(overImplied, underImplied);
        double marketJuice = marketJuice(totalImplied);
        double fairValue = overImplied / totalImplied;
        double EVPercentage = EVCalculation(fairValue, finalDecimal);

        return new double[]{fairValue, marketJuice, EVPercentage};
    }

    // Calculate fair values for each player and return results 
   public static Map<String, Map<String, Object>> calculatePerWebsite(
        Map<String, Map<String, List<Integer>>> overDict,
        Map<String, Map<String, List<Integer>>> underDict,
        Map<String, Map<String, List<Integer>>> finalDict) {

    Map<String, Map<String, Object>> returnValue = new HashMap<>();
    List<String> playerNames = new ArrayList<>(overDict.keySet());

    for (String player : playerNames) {
        List<Integer> overList = overDict.get(player).get("odd");
        List<Integer> underList = underDict.get(player).get("odd");
        List<Integer> finalList = finalDict.get(player).get("odd");

        List<Double> fairValueList = new ArrayList<>();
        List<Double> marketJuiceList = new ArrayList<>();
        List<Double> EVPercentageList = new ArrayList<>();

        Map<String, Object> goalOddsData = new HashMap<>();

        for (int i = 0; i < overList.size(); i++) {
            int over = overList.get(i);
            int under = underList.get(i);
            int finalOdds = finalList.get(i);

            if (over == 0 || under == 0 || finalOdds == 0) continue;

            double[] results = calculateFairValue(over, under, finalOdds);
            fairValueList.add(results[0]);
            marketJuiceList.add(results[1]);
            EVPercentageList.add(results[2]);
        }

        if (!fairValueList.isEmpty()) {
            double maxFairValue = Collections.max(fairValueList);
            int maxIndex = fairValueList.indexOf(maxFairValue);
            double maxEVPercentage = EVPercentageList.get(maxIndex); // Get EV percentage

            //  Ensure only good bets are sent (Fair Value > 0.5 AND EV > 0)
            if (maxFairValue > 0.5 && maxEVPercentage > 0) {
                goalOddsData.put("goal", overDict.get(player).get("goal"));
                goalOddsData.put("Leg Odds", overList.get(maxIndex) + " " + underList.get(maxIndex));
                goalOddsData.put("Final Odds", finalList.get(maxIndex));
                goalOddsData.put("Fair Value", fairValueList.get(maxIndex));
                goalOddsData.put("EV Percentage", EVPercentageList.get(maxIndex));
                goalOddsData.put("Market Juice", marketJuiceList.get(maxIndex));

                returnValue.put(player, goalOddsData);
            }
        }
    }

        return returnValue;
    }

}   
