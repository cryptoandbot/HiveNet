import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.*;

public class readJson {
    public static Map<String, Map<String, Map<String, List<Integer>>>> loadMockData(String filePath) {
        Gson gson = new Gson();
        try (FileReader reader = new FileReader(filePath)) {
            Type mapType = new TypeToken<Map<String, Map<String, Map<String, List<Integer>>>>>() {}.getType();
            return gson.fromJson(reader, mapType);
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }

    public static void main(String[] args) {
        String filePath = "mock_data.json"; // Ensure this file exists in your project root
        Map<String, Map<String, Map<String, List<Integer>>>> mockData = loadMockData(filePath);

        if (mockData != null) {
            Map<String, Map<String, List<Integer>>> overDict = mockData.get("over");
            Map<String, Map<String, List<Integer>>> underDict = mockData.get("under");
            Map<String, Map<String, List<Integer>>> finalDict = mockData.get("final");

            //  Pass data to EVCalculator
            Map<String, Map<String, Object>> results = EVCalc.calculatePerWebsite(overDict, underDict, finalDict);

            // Print results for verification
            System.out.println("=== EVCalculator Results ===");
            for (String player : results.keySet()) {
                System.out.println("Player: " + player);
                System.out.println("Fair Value: " + results.get(player).get("Fair Value"));
                System.out.println("EV Percentage: " + results.get(player).get("EV Percentage"));
                System.out.println("Market Juice: " + results.get(player).get("Market Juice"));
                System.out.println("=============================");
            }
        } else {
            System.out.println("Failed to load mock data.");
        }
    }
}
