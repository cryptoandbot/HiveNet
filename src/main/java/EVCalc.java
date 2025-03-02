import java.util.*;

public class EVCalc {
    // Convert American odds to decimal
    public static double convertOddsToDecimal(float americanOdds) {
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

    public static double[] calculateFairValue(float over, float under, float finalOdds) {
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

    // **Modified function: Now takes the full JSON data directly with PlayerData structure**
    public static void calculatePerWebsite(Map<String, Map<String, readJson.PlayerData>> jsonData) {
        // Ensure data exists
        if (!jsonData.containsKey("over") || !jsonData.containsKey("under") || !jsonData.containsKey("final")) {
            System.out.println("Invalid or missing data in JSON file.");
            return;
        }

        Map<String, readJson.PlayerData> overDict = jsonData.get("over");
        Map<String, readJson.PlayerData> underDict = jsonData.get("under");
        Map<String, readJson.PlayerData> finalDict = jsonData.get("final");

        Map<String, Map<String, Object>> returnValue = new HashMap<>();
        List<String> playerNames = new ArrayList<>(overDict.keySet());
        for (String player : playerNames) {
            readJson.PlayerData overData = overDict.get(player);
            readJson.PlayerData underData = underDict.get(player);
            readJson.PlayerData finalData = finalDict.get(player);
            if (overData == null || underData == null || finalData == null) continue;

            List<Integer> overList = overData.odd;
            List<Integer> underList = underData.odd;
            List<Integer> finalList = finalData.odd;

            if (overList == null || underList == null || finalList == null) continue;

            List<Double> fairValueList = new ArrayList<>();
            List<Double> marketJuiceList = new ArrayList<>();
            List<Double> EVPercentageList = new ArrayList<>();

            Map<String, Object> goalOddsData = new HashMap<>();

            for (int i = 0; i < overList.size(); i++) {
                float over = overList.get(i);
                float under = underList.get(i);
                float finalOdds = finalList.get(i);
//                System.out.println(over);
//                System.out.println(under);
//                System.out.println(finalOdds);
                if (over == 0 || under == 0 || finalOdds == 0) continue;

                double[] results = calculateFairValue(over, under, finalOdds);
                fairValueList.add(results[0]);
                marketJuiceList.add(results[1]);
                EVPercentageList.add(results[2]);
            }
//            System.out.println(fairValueList);
//            System.out.println(marketJuiceList);
//            System.out.println(EVPercentageList);
            if (!fairValueList.isEmpty()) {
                double maxFairValue = Collections.max(fairValueList);
                int maxIndex = fairValueList.indexOf(maxFairValue);
                double maxEVPercentage = EVPercentageList.get(maxIndex);

                // Ensure only good bets are sent (Fair Value > 0.5 AND EV > 0)
                if (maxFairValue > 0.5 && maxEVPercentage > 0) {
                    goalOddsData.put("goal", overData.goal);
                    goalOddsData.put("Leg Odds", overList.get(maxIndex) + " " + underList.get(maxIndex));
                    goalOddsData.put("Final Odds", finalList.get(maxIndex));
                    goalOddsData.put("Fair Value", fairValueList.get(maxIndex));
                    goalOddsData.put("EV Percentage", EVPercentageList.get(maxIndex));
                    goalOddsData.put("Market Juice", marketJuiceList.get(maxIndex));

                    returnValue.put(player, goalOddsData);
                }
            }
        }

        // Print results
        System.out.println("=== EV Calculation Results ===");
        for (String player : returnValue.keySet()) {
            System.out.println("Player: " + player);
            System.out.println("Goal: " + returnValue.get(player).get("goal"));
            System.out.println("Leg Odds: " + returnValue.get(player).get("Leg Odds"));
            System.out.println("Final Odds: " + returnValue.get(player).get("Final Odds"));
            System.out.println("Fair Value: " + returnValue.get(player).get("Fair Value"));
            System.out.println("EV Percentage: " + returnValue.get(player).get("EV Percentage"));
            System.out.println("Market Juice: " + returnValue.get(player).get("Market Juice"));
            System.out.println("=============================");
        }
    }
}
