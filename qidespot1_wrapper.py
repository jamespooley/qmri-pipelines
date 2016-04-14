import os
from nipype.interfaces.base import (TraitedSpec, CommandLineInputSpec,
                                    CommandLine, File)


class Qidespot1InputSpec(CommandLineInputSpec):
    in_spgr_file = File(exists=True,
                        desc='NIfTI file with SPGR pulse sequence data',
                        argstr='%s',
                        mandatory=True)  # position=-1 ??
    out_t1_file = File(desc='Map of T1 relaxation times',
                       argstr='%s',
                       hash_files=False,  # Look into hashing in nipype
                       mandatory=False,
                       name_template='%s_T1',  # Wrong!
                       name_source='in_file')  # Wrong!

    out_pd_file = File(desc='Calculated proton density map',
                       argstr='%s',
                       hash_files=False,  # Look into hasing in nipype
                       mandatory=False)

    print_help = traits.Bool(argstr='--help',
                             desc='Print usage information')
    verbose = traits.Bool(argstr='--verbose',
                          desc='Print more information')
    no_prompt = traits.Bool(argstr='--no-prompt',
                            desc='Suppress input prompts')
    mprage = traits.Bool(argstr='-M',
                         desc='Use a generic MP-RAGE sequence, not GE IR-SPGR')
    outname_prefix = traits.Str(argstr='--out %s',
                                desc='Add a prefix to the output filenames')
    mask = traits.File(argstr='--mask %s',
                       desc='Mask input with specified file')
    B1_map = traits.Bool(argstr='--B1 %s',
                         desc='B1 map file (ratio)')
    threshold = traits.Int(argstr='--thresh %d',
                           desc='Threshold maps at PD < n')
    clamp = traits.Int(argstr='-clamp %d',
                       desc='Clamp T1 between 0 and n')
    algorithm = traits.Enum('lls', 'wlls', 'nlls',
                            argstr='--algo %s',
                            desc='Fitting algorithm (default = LLS, only sensible option with only 2 flip angles)',
                            usedefault=True)
    max_iterations = traits.Int(15,
                                argstr='--its %d',
                                desc='Max iterations for WLLS/NLLS (default = 15),
                                usedefault=True)
    residuals = traits.Bool(argstr='--resids',
                            desc='Write out per flip angle residuals')
    n_threads = traits.Int(4,
                           argstr='--threads %d',
                           desc='Use N threads (default=hardware limit')  # TODO: set hardware limit as default
    # TODO: Find something to do about these two. This is wrong.
    TR = traits.Float(argstr='--TR',
                      desc='Repetition time')
    angles = traits.List(argstr='--angles',
                         desc='Flip angles (degrees)')



class Qidespot1OutputSpec(TraitedSpec):
    out_t1_file = File(desc='path/name of T1 map file')
    out_pd_file = File(desc='path/name of proton density map file')


class Qidespot1(CommandLine):
    """
    Perform Driven Equilibrium Single-Pulse Observation of T1 (DESPOT1)
    algorithm, also known as the Variable Flip-Angle (VFA) method. This is
    a fast way to measure
    longitudinal relaxation using a spoiled steady-state sequence, which is
    know by a different name by every scanner manufacturer just to be helpful.
    On GE, it's SPoiled Gradient Recalled echo (SPGR), on Siemens it's Fast
    Low-Angle SHot (FLASH) and on Phillips the sequence is Fast Field Echo
    (FFE).

    For more information: https://github.com/spinicist/QUIT/wiki/qidespot1

    Input
    =====
    A single NIfTI file containing at least 2 volumes, each acquired with a 
    different flip angle.

    Outputs
    =======
    - T1 map .nii file
    - Proton density map .nii file

    Important Options
    =================
    -a: This specifies which precise algorithm to use. There are 3 choices,
    classic linear least-squares (LLS), weighted linear least-squares (WLLS),
    and non-linear least-squares (NLLS). See Chang et al for a full discussion
    of the differences.

    Examples
    ========
    >>> from nipype.interfaces import quit
    >>> qidespot1 = quit.Qidespot1()
    >>> qidespot1.inputs.in_spgr_file = ...
    >>> qidespot1.inputs.no_prompt = '-n'
    >>>
    >>>
    >>>
    >>>
    >>>
    >>> ...
    >>> res = qidespot1.run()
    """

    _cmd = 'qidespot1'
    input_spec = Qidespot1InputSpec
    output_spec = Qidespot1OutputSpec

    # TODO: Overkill? Necessary? Wrong ... Probably wrong
    def _run_interface(self, runtime):
        runtime = super(Qidespot1, self)._runtime_interface(runtime)
        if runtime.stderr:
            self.raise_exceptions(runtime)
        return runtime

    def _format_arg(self, name, spec, value):
        if name == 'algo':  # --algo ?? change desc ??
            return spec.argstr % {'lls': 'l', 'wlls': 'w', 'nlls': 'n'}[value]
        return super(Qidespot1, self)._format_arg(name, spec, value)

    # TODO: wrong wrong wrong
    def _gen_outfilename(self):
        out_file = self.inputs.out_file
        if not isdefined(out_file) and isdefined(self.inputs.in_file):
            # TODO: _gen_fname only works with FSLCommand... I think
            out_file = self._gen_fname(self.inputs.in_file, suffix='_something')
        return os.path.abspath(out_file)

    # TODO: wrong wrong wrong
    # READ: https://neurostars.org/p/2834/
    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_t1_file'] = self._gen_outfilename()
        outputs['out_pd_file'] = self._gen_outfilename()
        return outputs
