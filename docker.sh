
docker run --volume="/scratch/jasperk/Siavash/NG-9864_MSL71_lib129294.fastq.gz:/bbx/input/reads.fq.gz:ro" --volume="/scratch/jasperk/Siavash/GalaxyBiobox/NG-9864_MSL71_lib129294/biobox.yaml:/bbx/input/biobox.yaml:ro" --volume="/scratch/jasperk/Siavash/GalaxyBiobox/NG-9864_MSL71_lib129294/bioboxes/soap:/bbx/output/:rw" --rm bioboxes/soap default
