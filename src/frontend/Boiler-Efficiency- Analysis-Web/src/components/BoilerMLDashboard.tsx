import { useState } from "react";
import svgPaths from "../imports/svg-nrl1h08m8q";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { toast } from "sonner@2.0.3";

type ModelType = "LightGBM" | "XGBoost" | "RandomForest" | "GradientBoosting";

interface Metrics {
  MAE: number;
  MSE: number;
  RMSE: number;
  R2: number;
  MAPE: number;
}

export default function BoilerMLDashboard() {
  const [startDate, setStartDate] = useState<string>("");
  const [endDate, setEndDate] = useState<string>("");
  const [selectedModel, setSelectedModel] = useState<ModelType>("LightGBM");
  const [estimators, setEstimators] = useState(200);
  const [maxDepth, setMaxDepth] = useState(3);
  const [subsample, setSubsample] = useState(0.5);
  const [colsample, setColsample] = useState(0.2);
  const [isDataLoaded, setIsDataLoaded] = useState(false);
  const [isTrained, setIsTrained] = useState(false);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [efficiencyData, setEfficiencyData] = useState<any[]>([]);
  const [featureImportance, setFeatureImportance] = useState<any[]>([]);

  const handleLoadData = () => {
    if (!startDate || !endDate) {
      toast.error("시작 날짜와 끝 날짜를 모두 선택해주세요.");
      return;
    }

    setTimeout(() => {
      const start = new Date(startDate);
      const end = new Date(endDate);
      const daysDiff = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
      const mockEfficiencyData = Array.from({ length: Math.min(daysDiff, 30) }, (_, i) => ({
        day: `Day ${i + 1}`,
        efficiency: 80 + Math.random() * 10,
      }));

      setEfficiencyData(mockEfficiencyData);
      setIsDataLoaded(true);
      toast.success("데이터가 성공적으로 로드되었습니다.");
    }, 1000);
  };

  const handleTrain = () => {
    if (!isDataLoaded) {
      toast.error("먼저 데이터를 로드해주세요.");
      return;
    }

    setTimeout(() => {
      const mockMetrics: Metrics = {
        MAE: 2.5 + Math.random() * 2,
        MSE: 8.2 + Math.random() * 3,
        RMSE: 2.9 + Math.random() * 1.5,
        R2: 0.85 + Math.random() * 0.1,
        MAPE: 3.2 + Math.random() * 2,
      };

      const mockFeatures = [
        { name: "입구 온도", importance: 0.25 + Math.random() * 0.1 },
        { name: "출구 온도", importance: 0.2 + Math.random() * 0.1 },
        { name: "압력", importance: 0.18 + Math.random() * 0.08 },
        { name: "유량", importance: 0.15 + Math.random() * 0.08 },
        { name: "연료 소비량", importance: 0.12 + Math.random() * 0.05 },
        { name: "산소 농도", importance: 0.1 + Math.random() * 0.05 },
      ].sort((a, b) => b.importance - a.importance);

      setMetrics(mockMetrics);
      setFeatureImportance(mockFeatures);
      setIsTrained(true);
      toast.success(`${selectedModel} 모델 학습이 완료되었습니다.`);
    }, 2000);
  };

  return (
    <div className="min-h-screen bg-[#2a2e2f] w-full overflow-y-auto">
      <div className="max-w-[1280px] mx-auto px-40 py-5">
        <div className="max-w-[960px] mx-auto">
          {/* Title */}
          <div className="mb-6">
            <h1 className="text-[#dcdad7] text-[32px] font-bold">Machine Learning Dashboard</h1>
          </div>

          {/* Data Selection Section */}
          <div className="mb-6">
            <h2 className="text-[#dcdad7] text-[22px] font-bold mb-4 px-4">Data Selection</h2>
            
            <div className="flex gap-4 px-4 mb-4">
              <div className="flex-1">
                <label className="text-[#dcdad7] text-[16px] mb-2 block">시작 날짜</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full h-14 px-4 bg-[#33383a] border border-[#37546f] rounded-lg text-[#7a9cbe] outline-none"
                />
              </div>
              <div className="flex-1">
                <label className="text-[#dcdad7] text-[16px] mb-2 block">끝 날짜</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  className="w-full h-14 px-4 bg-[#33383a] border border-[#37546f] rounded-lg text-[#7a9cbe] outline-none"
                />
              </div>
            </div>

            <div className="px-4">
              <button
                onClick={handleLoadData}
                className="bg-[#117ae2] text-[#dcdad7] px-6 py-3 rounded-lg hover:opacity-90 transition-opacity"
              >
                해당하는 데이터 로드
              </button>
            </div>
          </div>

          {/* Efficiency Chart Section */}
          <div className="mb-6 px-4">
            <h3 className="text-[#dcdad7] text-[16px] font-medium mb-2">보일러 효율</h3>
            {isDataLoaded && (
              <p className="text-[#dcdad7] text-[32px] font-bold mb-4">
                {(efficiencyData.reduce((acc, d) => acc + d.efficiency, 0) / efficiencyData.length).toFixed(1)}%
              </p>
            )}
            <div className="h-[200px] bg-[#1a1d1f] rounded-lg p-4">
              {isDataLoaded ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={efficiencyData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#37546f" />
                    <XAxis dataKey="day" stroke="#7a9cbe" />
                    <YAxis stroke="#7a9cbe" domain={[75, 95]} />
                    <Tooltip contentStyle={{ backgroundColor: '#2a2e2f', border: '1px solid #37546f' }} />
                    <Line type="monotone" dataKey="efficiency" stroke="#117ae2" strokeWidth={2} dot={{ fill: '#117ae2' }} />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-full text-[#7a9cbe]">
                  데이터를 로드해주세요
                </div>
              )}
            </div>
          </div>

          {/* Model Selection */}
          <div className="mb-6">
            <h2 className="text-[#dcdad7] text-[22px] font-bold mb-4 px-4">모델 선택</h2>
            <div className="grid grid-cols-4 gap-3 px-4">
              {[
                { value: "LightGBM" as ModelType, label: "LightGBM" },
                { value: "XGBoost" as ModelType, label: "XGBoost" },
                { value: "RandomForest" as ModelType, label: "Random Forest" },
                { value: "GradientBoosting" as ModelType, label: "Gradient Boosting Machine" },
              ].map((model) => (
                <div
                  key={model.value}
                  onClick={() => setSelectedModel(model.value)}
                  className="flex items-center gap-4 p-3 border border-[#37546f] rounded-lg cursor-pointer hover:bg-[#33383a] transition-colors"
                >
                  <div className="w-5 h-5 flex items-center justify-center">
                    {selectedModel === model.value ? (
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 20 20">
                        <circle cx="10" cy="10" r="9" stroke="#1280ED" strokeWidth="2" fill="none" />
                        <circle cx="10" cy="10" r="4" fill="#1280ED" />
                      </svg>
                    ) : (
                      <div className="w-5 h-5 border-2 border-[#37546f] rounded-full" />
                    )}
                  </div>
                  <span className="text-[#dcdad7] text-[14px]">{model.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Hyperparameter Tuning */}
          <div className="mb-6">
            <h2 className="text-[#dcdad7] text-[22px] font-bold mb-4 px-4">파라미터 튜닝</h2>
            
            <div className="space-y-4 px-4">
              {/* Estimators */}
              <div className="flex items-center gap-4">
                <label className="text-[#dcdad7] text-[16px] w-32">추정량</label>
                <input
                  type="range"
                  min="200"
                  max="30000"
                  value={estimators}
                  onChange={(e) => setEstimators(Number(e.target.value))}
                  className="flex-1 h-1 bg-[#37546f] rounded appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #117ae2 0%, #117ae2 ${((estimators - 200) / (30000 - 200)) * 100}%, #37546f ${((estimators - 200) / (30000 - 200)) * 100}%, #37546f 100%)`
                  }}
                />
                <span className="text-[#dcdad7] text-[14px] w-20 text-right">{estimators}</span>
              </div>

              {/* Max Depth */}
              <div className="flex items-center gap-4">
                <label className="text-[#dcdad7] text-[16px] w-32">트리 깊이</label>
                <input
                  type="range"
                  min="3"
                  max="30"
                  value={maxDepth}
                  onChange={(e) => setMaxDepth(Number(e.target.value))}
                  className="flex-1 h-1 bg-[#37546f] rounded appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #117ae2 0%, #117ae2 ${((maxDepth - 3) / (30 - 3)) * 100}%, #37546f ${((maxDepth - 3) / (30 - 3)) * 100}%, #37546f 100%)`
                  }}
                />
                <span className="text-[#dcdad7] text-[14px] w-20 text-right">{maxDepth}</span>
              </div>

              {/* Subsample */}
              <div className="flex items-center gap-4">
                <label className="text-[#dcdad7] text-[16px] w-32">행 샘플링</label>
                <input
                  type="range"
                  min="0.5"
                  max="1.0"
                  step="0.01"
                  value={subsample}
                  onChange={(e) => setSubsample(Number(e.target.value))}
                  className="flex-1 h-1 bg-[#37546f] rounded appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #117ae2 0%, #117ae2 ${((subsample - 0.5) / (1.0 - 0.5)) * 100}%, #37546f ${((subsample - 0.5) / (1.0 - 0.5)) * 100}%, #37546f 100%)`
                  }}
                />
                <span className="text-[#dcdad7] text-[14px] w-20 text-right">{subsample.toFixed(2)}</span>
              </div>

              {/* Colsample */}
              <div className="flex items-center gap-4">
                <label className="text-[#dcdad7] text-[16px] w-32">열 샘플링</label>
                <input
                  type="range"
                  min="0.2"
                  max="1.0"
                  step="0.01"
                  value={colsample}
                  onChange={(e) => setColsample(Number(e.target.value))}
                  className="flex-1 h-1 bg-[#37546f] rounded appearance-none cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, #117ae2 0%, #117ae2 ${((colsample - 0.2) / (1.0 - 0.2)) * 100}%, #37546f ${((colsample - 0.2) / (1.0 - 0.2)) * 100}%, #37546f 100%)`
                  }}
                />
                <span className="text-[#dcdad7] text-[14px] w-20 text-right">{colsample.toFixed(2)}</span>
              </div>
            </div>

            <div className="px-4 mt-4">
              <button
                onClick={handleTrain}
                disabled={!isDataLoaded}
                className="bg-[#117ae2] text-[#dcdad7] px-6 py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
              >
                모델 학습 시작
              </button>
            </div>
          </div>

          {/* Metrics Table */}
          <div className="mb-6">
            <h2 className="text-[#dcdad7] text-[22px] font-bold mb-4 px-4">공통 회귀 모델 평가 지표</h2>
            <div className="px-4">
              <div className="bg-[#1a1d1f] rounded-lg border border-[#37546f] overflow-hidden">
                <div className="grid grid-cols-4 bg-[#33383a]">
                  <div className="p-4 text-[#dcdad7] text-[14px] font-medium">Metric Name</div>
                  <div className="p-4 text-[#dcdad7] text-[14px] font-medium">설명</div>
                  <div className="p-4 text-[#dcdad7] text-[14px] font-medium">계산 방법</div>
                  <div className="p-4 text-[#dcdad7] text-[14px] font-medium">특징</div>
                </div>
                <div>
                  {/* MAE Row */}
                  <div className="grid grid-cols-4 border-t border-[#ccc9c5]">
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      <div className="font-medium mb-2">MAE</div>
                      {isTrained && metrics && (
                        <div className="text-[#7a9cbe]">{metrics.MAE.toFixed(2)}</div>
                      )}
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      실제값과 예측값의 차이를 절댓값으로 평균 낸 값.<br/>
                      예측 오차의 "평균적인 크기"를 직관적으로 보여 줌.
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      MAE = (1/n) Σ|yᵢ - ŷᵢ|
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      • 오차를 원 단위(효율 단위 그대로)로 해석 가능<br/>
                      • 이상치(극단값)에 대한 영향이 MSE/RMSE보다 덜 민감<br/>
                      • 0에 가까울수록 모델 성능이 좋음
                    </div>
                  </div>

                  {/* MSE Row */}
                  <div className="grid grid-cols-4 border-t border-[#ccc9c5]">
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      <div className="font-medium mb-2">MSE</div>
                      {isTrained && metrics && (
                        <div className="text-[#7a9cbe]">{metrics.MSE.toFixed(2)}</div>
                      )}
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      실제값과 예측값의 차이를 제곱해서 평균 낸 값.<br/>
                      큰 오차에 더 큰 페널티를 주는 지표.
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      MSE = (1/n) Σ(yᵢ - ŷᵢ)²
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      • 큰 오차를 강하게 벌주��� 때문에 이상치에 매우 민감<br/>
                      • 단위가 제곱 단위라 직관성은 다소 떨어짐<br/>
                      • 수학적으로 다루기 좋아서(미분 가능) 회귀 모델 학습에 자주 사용
                    </div>
                  </div>

                  {/* RMSE Row */}
                  <div className="grid grid-cols-4 border-t border-[#ccc9c5]">
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      <div className="font-medium mb-2">RMSE</div>
                      {isTrained && metrics && (
                        <div className="text-[#7a9cbe]">{metrics.RMSE.toFixed(2)}</div>
                      )}
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      MSE의 제곱근.<br/>
                      "제곱 오차 평균"을 다시 원래 단위로 돌린 값.
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      RMSE = √[(1/n) Σ(yᵢ - ŷᵢ)²]
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      • 해석 단위가 MAE처럼 원래 단위라 직관적<br/>
                      • 여전히 큰 오차에 민감(MSE와 비슷하게 이상치에 큰 영향)<br/>
                      • 실무에서 대표적인 기본 회귀 지표로 많이 사용
                    </div>
                  </div>

                  {/* R² Row */}
                  <div className="grid grid-cols-4 border-t border-[#ccc9c5]">
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      <div className="font-medium mb-2">R² (결정계수)</div>
                      {isTrained && metrics && (
                        <div className="text-[#7a9cbe]">{metrics.R2.toFixed(2)}</div>
                      )}
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      모델이 전체 변동성 중 얼마나 설명했는지를 나타내는 비율.<br/>
                      "설명력"이라고도 불림.
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      R² = 1 - [Σ(yᵢ - ŷᵢ)² / Σ(yᵢ - ȳ)²]
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      • 보통 0 ~ 1 사이(1에 가까울수록 설명력이 높음)<br/>
                      • 너무 나쁜 모델은 음수도 나올 수 있음<br/>
                      • 스케일에 독립적이라 데이터 단위가 달라도 비교 가능<br/>
                      • 변수 수가 증가하면 높아지는 경향 → 단순 비교 시 주의 필요
                    </div>
                  </div>

                  {/* MAPE Row */}
                  <div className="grid grid-cols-4 border-t border-[#ccc9c5]">
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      <div className="font-medium mb-2">MAPE</div>
                      {isTrained && metrics && (
                        <div className="text-[#7a9cbe]">{metrics.MAPE.toFixed(2)}%</div>
                      )}
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      실제값과 예측값의 차이를 실제값으로 나눈 비율의 절댓값 평균.<br/>
                      "평균적으로 몇 % 정도 틀렸는지"를 보여주는 지표.
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      MAPE = (100/n) Σ|((yᵢ - ŷᵢ) / yᵢ)|
                    </div>
                    <div className="p-4 text-[#dcdad7] text-[14px]">
                      • 퍼센트(%) 단위라 직관적이고 서로 다른 스케일의 문제 비교에 유용<br/>
                      • 실제값 yᵢ가 0이거나 0에 매우 가까우면 값이 폭발하거나 정의되지 않는 문제가 있음<br/>
                      • 작은 값(0에 가까운 %)일수록 좋은 모델
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Evaluation Metrics Performance Visualization */}
          <div className="mb-6 px-4">
            <h3 className="text-[#dcdad7] text-[16px] font-medium mb-4">Evaluation Metrics Performance</h3>
            <div className="grid grid-cols-5 gap-6">
              {/* MAE */}
              <div className="flex flex-col items-center gap-6">
                <div className="w-full h-[137px] bg-[#2c4257] border border-[#6b7478] rounded flex items-center justify-center">
                  {isTrained && metrics ? (
                    <div className="text-center">
                      <div className="text-[#7a9cbe] text-[13px] mb-2">MAE</div>
                      <div className="text-[#dcdad7] text-[24px] font-bold">{metrics.MAE.toFixed(2)}</div>
                    </div>
                  ) : (
                    <div className="text-[#7a9cbe] text-[13px]">이미지/차트 영역</div>
                  )}
                </div>
                <div className="text-[#7a9cbe] text-[13px] font-bold">MAE</div>
              </div>

              {/* MSE */}
              <div className="flex flex-col items-center gap-6">
                <div className="w-full h-[137px] bg-[#2c4257] border border-[#6b7478] rounded flex items-center justify-center">
                  {isTrained && metrics ? (
                    <div className="text-center">
                      <div className="text-[#7a9cbe] text-[13px] mb-2">MSE</div>
                      <div className="text-[#dcdad7] text-[24px] font-bold">{metrics.MSE.toFixed(2)}</div>
                    </div>
                  ) : (
                    <div className="text-[#7a9cbe] text-[13px]">이미지/차트 영역</div>
                  )}
                </div>
                <div className="text-[#7a9cbe] text-[13px] font-bold">MSE</div>
              </div>

              {/* RMSE */}
              <div className="flex flex-col items-center gap-6">
                <div className="w-full h-[137px] bg-[#2c4257] border border-[#6b7478] rounded flex items-center justify-center">
                  {isTrained && metrics ? (
                    <div className="text-center">
                      <div className="text-[#7a9cbe] text-[13px] mb-2">RMSE</div>
                      <div className="text-[#dcdad7] text-[24px] font-bold">{metrics.RMSE.toFixed(2)}</div>
                    </div>
                  ) : (
                    <div className="text-[#7a9cbe] text-[13px]">이미지/차트 영역</div>
                  )}
                </div>
                <div className="text-[#7a9cbe] text-[13px] font-bold">RMSE</div>
              </div>

              {/* R² */}
              <div className="flex flex-col items-center gap-6">
                <div className="w-full h-[137px] bg-[#2c4257] border border-[#6b7478] rounded flex items-center justify-center">
                  {isTrained && metrics ? (
                    <div className="text-center">
                      <div className="text-[#7a9cbe] text-[13px] mb-2">R²</div>
                      <div className="text-[#dcdad7] text-[24px] font-bold">{metrics.R2.toFixed(2)}</div>
                    </div>
                  ) : (
                    <div className="text-[#7a9cbe] text-[13px]">이미지/차트 영역</div>
                  )}
                </div>
                <div className="text-[#7a9cbe] text-[13px] font-bold">R²</div>
              </div>

              {/* MAPE */}
              <div className="flex flex-col items-center gap-6">
                <div className="w-full h-[137px] bg-[#2c4257] border border-[#6b7478] rounded flex items-center justify-center">
                  {isTrained && metrics ? (
                    <div className="text-center">
                      <div className="text-[#7a9cbe] text-[13px] mb-2">MAPE</div>
                      <div className="text-[#dcdad7] text-[24px] font-bold">{metrics.MAPE.toFixed(2)}%</div>
                    </div>
                  ) : (
                    <div className="text-[#7a9cbe] text-[13px]">이미지/차트 영역</div>
                  )}
                </div>
                <div className="text-[#7a9cbe] text-[13px] font-bold">MAPE</div>
              </div>
            </div>
          </div>

          {/* Feature Importance */}
          <div className="mb-6">
            <h2 className="text-[#dcdad7] text-[22px] font-bold mb-4 px-4">예상 효율 분석</h2>
            <div className="px-4">
              {isTrained ? (
                <div className="h-[300px] bg-[#1a1d1f] rounded-lg p-4">
                  <p className="text-[#dcdad7] text-[16px] mb-4">
                    효율에 가장 큰 영향을 미치는 인자 순위
                  </p>
                  <ResponsiveContainer width="100%" height={240}>
                    <BarChart data={featureImportance} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#37546f" />
                      <XAxis type="number" stroke="#7a9cbe" />
                      <YAxis dataKey="name" type="category" stroke="#7a9cbe" width={100} />
                      <Tooltip contentStyle={{ backgroundColor: '#2a2e2f', border: '1px solid #37546f' }} />
                      <Bar dataKey="importance" fill="#117ae2" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="text-[#dcdad7] text-[16px] px-4">학습 결과 표시 예정.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}