#cross validation visualizations
accuracy <- c(.754, .760, .776, .800, .793, .81,
             .817, .821, .803, .804, .806, .796,
             .823, .816, .825, .804, .808, .814,
             .814, .813)

precision <- c(.174, .174, .177, .259, .263,
               .126, .285, .133, .251, .229,
               .211, .227, .275, .266, .375,
               .167, .186, .253, .195, .324)

recall <- c(.165, .155, .115, .133, .159, .025,
            .063, .008, .094, .075, .062, .090,
            .022, .052, .046, .041, .039, .054,
            .030, .095)

f1 <- c(.170, .164, .140, .176, .198, .041,
        .103, .015, .136, .113, .096, .129,
        .041, .087, .081, .066, .065, .089,
        .053, .147)

measure_frame <- data.frame(
  Measure = c(rep('Accuracy', 20),
              rep('Precision', 20),
              rep('Recall', 20),
              rep('F1', 20)),
  Value = c(accuracy,
            precision,
            recall,
            f1)
)

library(ggplot2)

ggplot(measure_frame, aes(x=factor(Measure),
                          y=Value)) +
  geom_boxplot(fill="#1ca949") +
  ggtitle("SVC Cross-Validation Results") +
  xlab("Measure") +
  theme(plot.title = element_text(
          size=15, face = "bold"
        ))

summary_frame <- summary(accuracy)
summary_frame <- rbind(summary_frame, summary(precision))
summary_frame <- rbind(summary_frame, summary(recall))
summary_frame <- rbind(summary_frame, summary(f1))
rownames(summary_frame) <- c('Accuracy',
                             'Precision',
                             'Recall',
                             'F1')
summary_frame

top_terms <- read.csv('C://Users/cvint/Desktop/DSSG Unsafe Foods/github-unsafe-foods/DSSG2016-UnsafeFoods/github_data/words.csv')

library(wordcloud)

wordcloud(top_terms$word, freq = top_terms$coefficient, min.freq = 0,
          colors = brewer.pal(5, "Dark2"))
?brewer.pal
