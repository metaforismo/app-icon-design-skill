import SwiftUI

struct ContentView: View {
    var body: some View {
        ZStack {
            LinearGradient(
                colors: [Color(red: 0.08, green: 0.23, blue: 0.28), .black],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 16) {
                Image(systemName: "water.waves")
                    .font(.system(size: 54, weight: .semibold))
                Text("Quiet Tide")
                    .font(.largeTitle.bold())
                Text("Icon delivery fixture")
                    .foregroundStyle(.secondary)
            }
            .foregroundStyle(.white)
        }
    }
}
