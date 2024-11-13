[fname fpath]=uigetfile('*.txt');
gg=importdata([fpath,'/' fname]);
datafile = readmatrix([fpath,'/' fname],'NumHeaderLines',53);
[Ro Co] = size(datafile);
sumdata = zeros(Ro,2);


for i = 1:Ro
    sumdata(i,1) = datafile(i,1);
    for j = 2:(Co-1)
        sumdata(i,2) = datafile(i,j)+sumdata(i,2);
    end
end
BindingEnergy =sumdata(:,1);
Intensity = sumdata(:,2);
Intensity = Intensity - min(Intensity);
Intensity = Intensity./max(Intensity);
hold on;
plot(BindingEnergy,Intensity);
hold on;
xlabel("Binding Energy (eV)");
ylabel("Intensity (a.u.)");