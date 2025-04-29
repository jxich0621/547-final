#include "Instrument.h"

using namespace llvm;

namespace instrument {

static const char *SANITIZE_DIV_FUNCTION_NAME = "__sanitize_div__";
static const char *SANITIZE_NULL_PTR_FUNCTION_NAME = "__sanitize_nullptr__";
static const char *SANITIZE_ASSERT_FUNCTION_NAME = "__sanitize_assert__";
static const char *COVERAGE_FUNCTION_NAME = "__coverage__";
static const char *ASSERT_FUNCTION_NAME = "__assert_fail";

void instrumentCoverage(Module *M, Instruction &I, int Line, int Col) {
  auto &Context = M->getContext();
  Type *Int32Type = Type::getInt32Ty(Context);

  auto *LineVal = llvm::ConstantInt::get(Int32Type, Line);
  auto *ColVal = llvm::ConstantInt::get(Int32Type, Col);
  std::vector<Value *> Args = {LineVal, ColVal};

  auto *Fun = M->getFunction(COVERAGE_FUNCTION_NAME);
  CallInst::Create(Fun, Args, "", &I);
}

void instrumentSanitizeDiv(Module *M, Instruction &I, int Line, int Col) {
  LLVMContext &Context = M->getContext();
  Type *Int32Type = Type::getInt32Ty(Context);

  auto *Divisor = I.getOperand(1);
  auto *LineVal = llvm::ConstantInt::get(Int32Type, Line);
  auto *ColVal = llvm::ConstantInt::get(Int32Type, Col);
  std::vector<Value *> Args = {Divisor, LineVal, ColVal};

  auto *Fun = M->getFunction(SANITIZE_DIV_FUNCTION_NAME);
  CallInst::Create(Fun, Args, "", &I);
}

void instrumentSanitizeNullPtr(Module *M, Instruction &I, int Line, int Col) {
  LLVMContext &Context = M->getContext();
  Type *Int32Type = Type::getInt32Ty(Context);

  Value *Ptr = nullptr;

  if (auto *LI = dyn_cast<LoadInst>(&I)) {
    Ptr = LI->getPointerOperand();
  } else if (auto *SI = dyn_cast<StoreInst>(&I)) {
    Ptr = SI->getPointerOperand();
  }


  auto *LineVal = ConstantInt::get(Int32Type, Line);
  auto *ColVal  = ConstantInt::get(Int32Type, Col);

  IRBuilder<> Builder(&I);
  Value *Casted = Builder.CreateBitCast(Ptr, Type::getInt8PtrTy(Context));

  std::vector<Value *> Args = {Casted, LineVal, ColVal};

  auto *Fun = M->getFunction(SANITIZE_NULL_PTR_FUNCTION_NAME);
  
  CallInst::Create(Fun, Args, "", &I);

}

void instrumentAssert(Module *M, Instruction &I, int Line, int Col) {
  LLVMContext &Context = M->getContext();
  Type *Int32Type = Type::getInt32Ty(Context);

  Value *ExprStr = nullptr;
  if (auto *call = dyn_cast<CallInst>(&I)) {
    if (call->getNumArgOperands() >= 1) {
      ExprStr = call->getArgOperand(0); 
    }
  }

  if (!ExprStr) {
    errs() << "Warning: Could not extract assertion string!\n";
    return;
  }

  Value *LineVal = ConstantInt::get(Int32Type, Line);
  Value *ColVal  = ConstantInt::get(Int32Type, Col);

  std::vector<Value *> Args = {ExprStr, LineVal, ColVal};
  auto *Fun = M->getFunction(SANITIZE_ASSERT_FUNCTION_NAME);
  
  CallInst::Create(Fun, Args, "", &I);
}

bool Instrument::runOnFunction(Function &F) {
  LLVMContext &Context = F.getContext();
  Module *M = F.getParent();

  Type *VoidType = Type::getVoidTy(Context);
  Type *Int32Type = Type::getInt32Ty(Context);
  Type *VoidPtrTy = Type::getInt8PtrTy(Context);

  M->getOrInsertFunction(COVERAGE_FUNCTION_NAME, VoidType, Int32Type,
                         Int32Type);
  M->getOrInsertFunction(SANITIZE_DIV_FUNCTION_NAME, VoidType, Int32Type, Int32Type,
                         Int32Type);
  M->getOrInsertFunction(SANITIZE_NULL_PTR_FUNCTION_NAME, VoidType, VoidPtrTy,
                         Int32Type, Int32Type);
  M->getOrInsertFunction(SANITIZE_ASSERT_FUNCTION_NAME, VoidType, VoidPtrTy,
                          Int32Type, Int32Type); 

  for (inst_iterator I = inst_begin(F), E = inst_end(F); I != E; ++I) {
    if (I->getOpcode() == Instruction::PHI) {
      continue;
    }
    const auto DebugLoc = I->getDebugLoc();
    if (!DebugLoc) {
      continue;
    }
    int Line = DebugLoc.getLine();
    int Col = DebugLoc.getCol();
    if (I->getOpcode() == Instruction::SDiv ||
        I->getOpcode() == Instruction::UDiv) {
      instrumentSanitizeDiv(M, *I, Line, Col);
    }

    if (isa<LoadInst>(&*I) || isa<StoreInst>(&*I)) {
      instrumentSanitizeNullPtr(M, *I, Line, Col); 
    }

    if (auto *call = dyn_cast<CallInst>(&*I)) {
      if (Function *callee = call->getCalledFunction()) {
          if (callee->getName() == "__assert_fail") {
              instrumentAssert(M, *call, Line, Col);
          }
      }
    }


    instrumentCoverage(M, *I, Line, Col);
  }
  return true;
}

char Instrument::ID = 1;
static RegisterPass<Instrument>
    X("Instrument", "Instrumentations for Dynamic Analysis", false, false);

} // namespace instrument
